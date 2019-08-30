import pdb
import thread
import threading
import time

import config
import constants
from car import HierarchicalCar
import topic_program
import utils
import theano

class Simulator(object):
    # Simulate the world by getting the car controls, applying them to move the
    # cars, and updating the simulation time.
    def __init__(self, world, dt, feed_u=None, interaction_data=None):
        """
        world: the world to simulate
        dt: timestepe
        feed_u: list of fed-in controls for each car
        interaction_data: data describing the saved interaction to simulate
        """
        self.world = world
        self.dt = dt
        self.time = 0 # simulation time
        self.feed_u = feed_u
        self.interaction_data = interaction_data
        self.rewards = [0.0, 0.0, 0.0]

    def simulate(self):
        """Get the car controls, move the cars, update time."""
        print 'time: {0}'.format(self.time)
        if self.interaction_data is None:
            plans = self.plan()
            controls = [plan[0] for plan in plans] # first control in plan
            self.step(controls)
        else:
            self.set_states()
        self.time += self.dt


    def plan(self):
        """Generates new plans for each car."""
        # Update trajectory information of the other car for each car
        for car in self.world.cars:
            car.update_other_traj()

        plans = []
        if self.feed_u is None:
            for car in self.world.cars:
                # use current stored plan for user-controlled cars (whose controls
                # are set by user input) and for follower cars (whose controls)
                # are set by the robot.
                if car.is_user_controlled or car.is_follower:
                    plan = car.traj.u 
                else: # Only non-user-controlled cars generate plans
                    plan = car.plan()
                plans.append(plan)
        else: # use plan that was fed in
            for car, controls in zip(self.world.cars, self.feed_u):
                control = controls[len(car.history)]
                car.set_control(control)
                plans.append([control])
        
        # Append Sample to cars' interaction history
        for car, plan in zip(self.world.cars, plans):
            tact_r = None # tactical reward
            if car.reward is not None:
                tact_r = car.reward.reward_np(0, car.traj.x0, plan[0])
            if isinstance(car, HierarchicalCar):
                # compute strategic value for HierarchicalCar
                strat_val = car.strat_val.value_r_np(self.time, car.traj.x0, 
                                                    car.traj.u[0])
                sample = utils.HierarchicalCarSample(
                    self.time, car.traj.x0, plan, car.traj_h.u, tact_r, strat_val)
            elif hasattr(car, 'traj_h'):
                sample = utils.NestedCarSample(
                    self.time, car.traj.x0, plan, car.traj_h.u, tact_r)
            else:
                sample = utils.Sample(self.time, car.traj.x0, plan, tact_r)
            car.history.append(sample)

        return plans

    def step(self, controls):
        """Move the cars by applying the given controls."""
        assert(len(controls) == len(self.world.cars))
        if not config.ASYNCHRONOUS:
            for car, control in zip(self.world.cars, controls):
                car.move(control)
                # print('{0} x: {1}'.format(car.name, car.traj.x0[0]))
                # print('{0} y: {1}'.format(car.name, car.traj.x0[1]))
                # print('{0} heading: {1}'.format(car.name, car.traj.x0[2]))
                # print('{0} speed: {1}'.format(car.name, car.traj.x0[3]))

    def set_states(self):
        """Set the car states to those described in the interaction data."""
        index = int(self.time / self.dt)
        if index >= len(self.interaction_data[0]):
            print 'Finished interaction data. Pausing.'
            topic_program.paused = True
            print("Robot Rewards, Robot_Human Rewards, Human_Human Rewards", self.rewards)
            return
        else:
            for car, car_interaction_data in zip(self.world.cars, self.interaction_data):
                car.traj.x0 = car_interaction_data[index][1] # TODO: make this depend on the time stored in the interaction data (use bisect)
                car.traj.u = car_interaction_data[index][2]


                if hasattr(car, 'traj_h'):
                    car.traj_h.u = car_interaction_data[index][3]

                # debugging
                # print('{0} x: {1}'.format(car.name, car.traj.x0[0]))
                print('{0} y: {1}'.format(car.name, car.traj.x0[1]))
                # print('{0} heading: {1}'.format(car.name, car.traj.x0[2]))
                # print('{0} speed: {1}'.format(car.name, car.traj.x0[3]))
            # Update position of the robot car's belief of the human trajectory
            # (must be done after updating the human's actual trajectory)
            for car in self.world.cars:
                if hasattr(car, 'human') and hasattr(car, 'traj_h'):
                    car.traj_h.x0 = car.human.traj.x0
            #
            # for car in self.world.cars:
            #     if car is self.world.main_human_car:
            #         h_h = car.reward.reward_th(0, car.traj.x0, car.traj.u[0])
            #         self.rewards[2] += theano.function([], [h_h])()[0]
            #     if car is self.world.main_robot_car:
            #         r_r = car.reward.reward_th(0, car.traj.x0, car.traj.u[0])
            #         self.rewards[0] += theano.function([], [r_r])()[0]
            #         # r_h = car.reward_h.reward_th(0, car.traj_h.x0, car.traj_h.u[0])
            #         # self.rewards[1] += theano.function([], [r_h])()[0]
            # print(self.rewards)


