import pdb
import numpy as np
import theano.tensor as tt

import config
import constants
from optimizer import Maximizer, NestedMaximizer, HierarchicalMaximizer, PredictReactMaximizer, PredictReactHierarchicalMaximizer, IteratedBestResponseMaximizer, ILQRMaximizer
from planner import Planner, TwoCarPlanner, FixedControlPlanner
from trajectory import Trajectory
import utils
import torch


class Car(object):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name):
        # Non-obvious arguments:
        #  - x0: initial state
        #  - dyn: dynamics class. Needs to be initialized to get dynamcis function.
        self.dt = dt
        self.bounds = bounds
        self.color = color
        self.name = name
        self.horizon = horizon
        self.traj = Trajectory(x0, dyn, dt, horizon)
        # Trajectory produced by applying zero control from current state
        self.traj_linear = Trajectory(x0, dyn, dt, horizon)
        self.history = [] # list of Sample
        self.reward = None # car-specific
        self.planner = None # car-specific
        self.dyn = dyn
    
    def reset(self, x0=None):
        # Reset car to given position, or to the car's initial position if x0 is None.
        self.traj.reset(x0)
        self.traj_linear.reset(x0)
        self.history = []
        if hasattr(self, 'traj_h'):
            self.traj_h.reset()
        if hasattr(self, 'traj_r'):
            self.traj_r.reset()

    def set_control(self, control):
        # Set the plan (self.traj.u) to just one control action, with the default
        # action appended to the end.
        new_u = np.array([self.traj.default_control for i in range(self.horizon)])
        new_u[0] = control
        self.traj.u = new_u
        self.traj.u_th = new_u

    def plan(self):
        # Generate a new plan.
        return self.planner.plan() # Saves new plan in self.traj

    def move(self, control=None):
        # Move the car by applying the given control, or the first control in
        # the car's plan if no control is given.
        if control is None:
            control = self.traj.u[0]
        self.traj.move(control=control)
        self.traj_linear.move(control=control)
        # TODO: is this right?
        if hasattr(self, 'human') and hasattr(self, 'traj_h'):
            self.traj_h.move()
        if hasattr(self, 'robot') and hasattr(self, 'traj_r'):
            self.traj_r.move()

    def update_other_traj(self):
        """Update this car's knowledge of other trajectories with the current
        positions of those vehicles."""
        if hasattr(self, 'human') and hasattr(self, 'traj_h'):
            self.traj_h.x0 = self.human.traj.x0
            self.traj_h.x0_th = self.human.traj.x0
        if hasattr(self, 'robot') and hasattr(self, 'traj_r'):
            self.traj_r.x0 = self.robot.traj.x0
            self.traj_r.x0_th = self.robot.traj.x0
        if hasattr(self, 'truck') and hasattr(self, 'traj_truck'):
            self.traj_truck.x0 = self.truck.traj.x0
            self.traj_truck.x0_th = self.truck.traj.x0


    @property
    def truck(self):
        return self._truck   
    @truck.setter
    def truck(self, value):
        self._truck = value
        self.name_truck = self._truck.name
        self.traj_truck = self._truck.traj # car knows the truck trajectory
        

class UserControlledCar(Car):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name):
        Car.__init__(self, x0, dt, dyn, bounds, horizon, color, name)
        self.is_robot = False
        self.is_user_controlled = True
        self.is_follower = False


class RobotCar(Car):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name):
        Car.__init__(self, x0, dt, dyn, bounds, horizon, color, name)
        self.is_robot = True
        self.is_user_controlled = False
        self.is_follower = False
        self.reward_h = None # reward of the human

    @property
    def human(self):
        return self._human   
    @human.setter
    def human(self, value):
        self._human = value
        self.name_h = self._human.name
        self.traj_h = Trajectory(self._human.traj.x0, self._human.traj.dyn, 
            self._human.traj.dt, self._human.horizon)

class MaintainSpeedCar(RobotCar):
    def init_planner(self, init_plan_scheme):
        fixed_control = [0., constants.FRICTION * self.traj.x0[3]**2]
        self.planner = FixedControlPlanner(self.traj, fixed_control)

class SimpleOptimizerCar(RobotCar):
    def init_planner(self, init_plan_scheme=None):
        # Initialize the planner with the optimizer.
        r = self.traj.reward(self.reward.reward_th, fw=tt)
        self.optimizer = Maximizer(r, self.traj.u_th)
        self.planner = Planner(self.traj, self.optimizer, self.bounds, 
                               name=self.name)


class BadOptimizerCar(RobotCar):
    def init_planner(self, init_plan_scheme):
        r_h = self.traj_h.reward(self.reward_h.reward_th, fw=tt)
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)

        self.optimizer = IteratedBestResponseMaximizer\
                (
            r_h, self.traj_h, r_r, self.traj,
            init_plan_scheme=init_plan_scheme)

        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
                                     self.optimizer, self.bounds, name=self.name)


class FollowerCar(Car):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name):
        Car.__init__(self, x0, dt, dyn, bounds, horizon, color, name)
        self.is_robot = False
        self.is_user_controlled = False
        self.is_follower = True
    
    @property
    def robot(self):
        return self._robot   
    @robot.setter
    def robot(self, value):
        self._robot = value
        self.traj = self._robot.traj_h
        self.traj_linear = self._robot.traj_h

    def move(self, control=None):
        # No movement implemented here because the FollowerCar's trajectory is
        # controlled by the robot's predictions of its trajectory.
        pass

class NestedCar(RobotCar):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name, use_second_order):
        # Non-obvious arguments:
        #  - use_second_order: if True, use Hessian for optimization
        RobotCar.__init__(self, x0, dt, dyn, bounds, horizon, color, name)
        self.use_second_order = use_second_order

    def init_planner(self, init_plan_scheme):
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)
        r_h = self.traj_h.reward(self.reward_h.reward_th, fw=tt)
        # self.optimizer = NestedMaximizer(
        #     r_h, self.traj_h, r_r, self.traj, 
        #     use_second_order=self.use_second_order)

        self.optimizer = NestedMaximizer(
            r_h, self.traj_h, r_r, self.traj, 
            use_second_order=self.use_second_order,
            init_plan_scheme=init_plan_scheme)
        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
            self.optimizer, self.bounds, name=self.name)

class IteratedBestResponseCar(RobotCar):
    def init_planner(self, init_plan_scheme):
        r_h = self.traj_h.reward(self.reward_h.reward_th, fw = tt)
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)

        self.optimizer = IteratedBestResponseMaximizer\
                (
            r_h, self.traj_h, r_r, self.traj,
            init_plan_scheme=init_plan_scheme)

        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
                                     self.optimizer, self.bounds, name=self.name)
        #self.planner = Planner(self.traj, self.optimizer, self.bounds,
                               #name=self.name)


class PredictReactCar(NestedCar):
    def init_planner(self, init_plan_scheme):
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)

        if config.PREDICT_HUMAN_IGNORES_ROBOT:
            # Predict that human's reward is independent of the robot's trajectory
            # (i.e. human ignores the robot).
            r_h = self.traj_h.reward(self.reward_h_ignore_robot.reward_th, fw=tt)
        else:
            # Predict that human's reward is not independent of the robot's
            # trajectory (i.e. the robot's prediction of the human will rely
            # on how it chooses to initialize the human's belief of the robot's
            # plan).
            r_h = self.traj_h.reward(self.reward_h.reward_th, fw=tt)
        
        self.optimizer = PredictReactMaximizer(
            r_h, self.traj_h, r_r, self.traj, 
            use_second_order=self.use_second_order,
            init_plan_scheme=init_plan_scheme)
        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
            self.optimizer, self.bounds, name=self.name)

class HierarchicalCar(NestedCar):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name, 
            mat_name, use_second_order, proj, strat_dim):
        # Non-obvious arguments:
        #  - mat_name: name of matlab
        #  - use_second_order: if True, use Hessian for optimization
        #  - proj: state projection from tactical to strategic domain
        #  - strat_dim: dimension of the strategic state
        NestedCar.__init__(self, x0, dt, dyn, bounds, horizon, color, name, use_second_order)
        self.mat_name = mat_name
        self.proj = proj
        self.strat_dim = strat_dim

    def init_planner(self, init_plan_scheme):
        self.traj_truck = None
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)
        r_h = self.traj_h.reward(self.reward_h.reward_th, fw=tt)
        self.optimizer = HierarchicalMaximizer(
            r_h, self.traj_h, r_r, self.traj, 
            mat_name=self.mat_name, n=self.strat_dim, proj=self.proj.proj_th,
            traj_truck=self.traj_truck,
            use_second_order=self.use_second_order,
            init_plan_scheme=init_plan_scheme)
        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
            self.optimizer, self.bounds, name=self.name)

class PredictReactHierarchicalCar(HierarchicalCar):
    def init_planner(self, init_plan_scheme):
        r_r = self.traj.reward(self.reward.reward_th, fw=tt)

        if config.PREDICT_HUMAN_IGNORES_ROBOT:
            # Predict that human's reward is independent of the robot's trajectory
            # (i.e. human ignores the robot).
            r_h = self.traj_h.reward(self.reward_h_ignore_robot.reward_th, fw=tt)
        else:
            # Predict that human's reward is not independent of the robot's
            # trajectory (i.e. the robot's prediction of the human will rely
            # on how it chooses to initialize the human's belief of the robot's
            # plan).
            r_h = self.traj_h.reward(self.reward_h.reward_th, fw=tt)

        if not hasattr(self, 'traj_truck'):
            self.traj_truck = None

        self.optimizer = PredictReactHierarchicalMaximizer(
            r_h, self.traj_h, r_r, self.traj, 
            mat_name=self.mat_name, n=self.strat_dim, proj=self.proj.proj_th,
            traj_truck=self.traj_truck,
            use_second_order=self.use_second_order,
            init_plan_scheme=init_plan_scheme)

        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
            self.optimizer, self.bounds, name=self.name)


class ILQRCar(RobotCar):
    def init_planner(self, init_plan_scheme):
        r_h = self.traj_h.reward(self.reward_h.reward_torch, fw=torch)
        r_r = self.traj.reward(self.reward.reward_torch, fw=torch)

        self.optimizer = ILQRMaximizer (
                self.reward_h, self.traj_h, self.reward, self.traj, self.dyn)

        self.planner = TwoCarPlanner(self.traj, self.traj_h, self.human,
            self.optimizer, self.bounds, name=self.name)





class Truck(Car):
    def __init__(self, x0, dt, dyn, bounds, horizon, color, name):
        Car.__init__(self, x0, dt, dyn, bounds, horizon, color, name)
        self.is_robot = False
        self.is_user_controlled = False
        self.is_follower = False

    def init_planner(self, init_plan_scheme):
        # Apply control needed to maintain initial speed.
        fixed_control = [0., constants.FRICTION * self.traj.x0[3]**2]
        self.planner = FixedControlPlanner(self.traj, fixed_control)
