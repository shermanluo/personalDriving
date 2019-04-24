import reward
import utils
from trajectory import Trajectory
import time

################################################################################
#### Demanding controllers that can be shared between vehicles are put here ####
################################################################################

class TruckAttentiveController(object):
    # This the shared DSG/MPC controller for the follower trucks.
    # The leader has always just a simple maximizer.
    def __init__(self,lanes,fences,use_DSG):
        self.truck = None
        self.predecessor = None
        self.maniac = None
        self.lanes = lanes
        self.fences = fences
        self.use_DSG = use_DSG
        self.bounds = None
        self.human_bounds = None
        self.optimizer_follower = None

    @property
    def human(self):
        return self._human
    @human.setter
    def human(self, value):
        self._human = value
        self.traj_h = Trajectory(self.human.T, self.human.dyn)

    def initialize(self):
        if self.optimizer_follower is None:

            if self.maniac is not None: # Have a maniac.

                # For the following truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=self.predecessor)
                reward_r_critical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=self.predecessor)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) #world.cars[0].bounds)
                reward_h_critical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) #world.cars[0].bounds)

                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_r_critical = self.truck.traj.reward(reward_r_critical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)
                reward_h_critical = self.traj_h.reward(reward_h_critical)

                self.optimizer_follower = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u), utils.NestedMaximizer(reward_h_critical, self.traj_h.u, reward_r_critical, self.truck.traj.u)]

            else: # No maniac.
                
                # For the following truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, predecessor=self.predecessor)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) # have bounds=None on original.

                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)

                self.optimizer_follower = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u)]

    def optimize(self,truck):

        # 1. UPDATE.
        # Update state and control for current truck.
        self.truck.traj.x0.set_value(truck.traj.x0.get_value())
        for i in range(len(truck.traj.u)):
            self.truck.traj.u[i].set_value(truck.traj.u[i].get_value())
        # Update state and control for preceeeding truck.
        self.predecessor.traj.x0.set_value(truck.predecessor.traj.x0.get_value())
        for i in range(len(truck.traj.u)):
            self.predecessor.traj.u[i].set_value(truck.predecessor.traj.u[i].get_value())
        # Update state and control for human.
        self.traj_h.x0.set_value(self.human.x)
        for i in range(len(truck.traj_h.u)):
            self.traj_h.u[i].set_value(truck.traj_h.u[i].get_value())

        # 2. OPTIMIZE.
        if self.maniac is None:
            crash_time = -1 # will never happen.
        else:
            crash_time = (self.maniac.x[1]-self.human.x[1])/(abs(self.maniac.x[3])+abs(self.human.x[3]))
        if crash_time <= 5.5 and 0.5 <= crash_time:
            self.optimizer_follower[1].maximize(bounds = self.bounds) # critical control.
        else:
            self.optimizer_follower[0].maximize(bounds = self.bounds) # noncritical control.

        # 3. SET CONTROLS FOR THE REAL TRUCK.
        for i in range(len(truck.traj.u)):
            truck.traj.u[i].set_value(self.truck.traj.u[i].get_value())
        for i in range(len(truck.traj_h.u)):
            truck.traj_h.u[i].set_value(self.traj_h.u[i].get_value())

class TruckAttentiveController_deb(object):
    # This the shared DSG/MPC controller for the follower trucks.
    # The leader has a nested maximizer as well.
    def __init__(self,lanes,fences,use_DSG):
        self.truck = None
        self.predecessor = None
        self.maniac = None
        self.lanes = lanes
        self.fences = fences
        self.use_DSG = use_DSG
        self.bounds = None
        self.human_bounds = None
        self.optimizer_leader = None
        self.optimizer_follower = None

    @property
    def human(self):
        return self._human
    @human.setter
    def human(self, value):
        self._human = value
        self.traj_h = Trajectory(self.human.T, self.human.dyn)

    def initialize(self):
        if self.optimizer_leader is None and self.optimizer_follower is None:

            if self.maniac is not None: # Have a maniac.

                # For the leading truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=None)
                reward_r_critical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=None)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=None, bounds=self.human_bounds) #world.cars[0].bounds)
                reward_h_critical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=None, bounds=self.human_bounds) #world.cars[0].bounds)
                
                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_r_critical = self.truck.traj.reward(reward_r_critical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)
                reward_h_critical = self.traj_h.reward(reward_h_critical)

                self.optimizer_leader = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u), utils.NestedMaximizer(reward_h_critical, self.traj_h.u, reward_r_critical, self.truck.traj.u)]

                # For the following truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=self.predecessor)
                reward_r_critical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, predecessor=self.predecessor)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) #world.cars[0].bounds)
                reward_h_critical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = True, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=self.maniac.traj, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) #world.cars[0].bounds)

                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_r_critical = self.truck.traj.reward(reward_r_critical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)
                reward_h_critical = self.traj_h.reward(reward_h_critical)

                self.optimizer_follower = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u), utils.NestedMaximizer(reward_h_critical, self.traj_h.u, reward_r_critical, self.truck.traj.u)]

            else: # No maniac.

                # For the leading truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, predecessor=None)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, lanes=self.lanes, fences=self.fences, predecessor=None, bounds=self.human_bounds) # have bounds=None on original.

                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)
                
                self.optimizer_leader = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u)]
                
                # For the following truck.
                reward_r_noncritical = reward.attentive_truck_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, predecessor=self.predecessor)
                reward_h_noncritical = reward.attentive_human_reward(use_DSG = self.use_DSG, critical = False, truck_traj=self.truck.traj, human_traj=self.traj_h, maniac_traj=None, lanes=self.lanes, fences=self.fences, predecessor=self.predecessor, bounds=self.human_bounds) # have bounds=None on original.

                reward_r_noncritical = self.truck.traj.reward(reward_r_noncritical)
                reward_h_noncritical = self.traj_h.reward(reward_h_noncritical)

                self.optimizer_follower = [utils.NestedMaximizer(reward_h_noncritical, self.traj_h.u, reward_r_noncritical, self.truck.traj.u)]

    def optimize(self,truck):

        start = time.time()
        # 1. UPDATE
        # Update state and control for current truck.
        self.truck.traj.x0.set_value(truck.traj.x0.get_value())
        for i in range(len(truck.traj.u)):
            self.truck.traj.u[i].set_value(truck.traj.u[i].get_value())
        # Update state and control for preceeeding truck.
        if truck.predecessor is not None:
            self.predecessor.traj.x0.set_value(truck.predecessor.traj.x0.get_value())
            for i in range(len(truck.traj.u)):
                self.predecessor.traj.u[i].set_value(truck.predecessor.traj.u[i].get_value())
        # Update state and control for human.
        self.traj_h.x0.set_value(self.human.x)
        for i in range(len(truck.traj_h.u)):
            self.traj_h.u[i].set_value(truck.traj_h.u[i].get_value())
        end = time.time()
        print(end-start)

        start = time.time()
        # 2. OPTIMIZE
        if self.maniac is None:
            crash_time = -1 # will never happen.
        else:
            crash_time = (self.maniac.x[1]-self.human.x[1])/(abs(self.maniac.x[3])+abs(self.human.x[3]))
        if self.predecessor is not None:
            if crash_time <= 5.5 and 0.5 <= crash_time:
                self.optimizer_follower[1].maximize(bounds = self.bounds) # critical control.
            else:
                print('inner loop:')
                start1 = time.time()
                self.optimizer_follower[0].maximize(bounds = self.bounds) # noncritical control.
                end1 = time.time()
                print(end1-start1)
        else:
            if crash_time <= 5.5 and 0.5 <= crash_time:
                self.optimizer_leader[1].maximize(bounds = self.bounds) # critical control.
            else:
                self.optimizer_leader[0].maximize(bounds = self.bounds) # noncritical control.
        # Now self.truck has an updated control.
        end = time.time()
        print(end-start)

        start = time.time()
        # 3. SET CONTROLS FOR THE REAL TRUCK
        for i in range(len(truck.traj.u)):
            truck.traj.u[i].set_value(self.truck.traj.u[i].get_value())
        for i in range(len(truck.traj_h.u)):
            truck.traj_h.u[i].set_value(self.traj_h.u[i].get_value())
        end = time.time()
        print(end-start)

