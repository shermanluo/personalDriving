import pdb
import sys

import numpy as np
import theano.tensor as tt

import config
import constants
import feature
import utils

class Reward(object):
    def __init__(self, world, other_car_trajs, other_truck_trajs=[],
            w_lanes=None, w_fences=None, w_speed=config.W_SPEED, 
            w_other_car_trajs=None, w_other_truck_trajs=None,
            w_behind=config.W_BEHIND, w_control=config.W_CONTROL,
            w_bounded_control=config.W_BOUNDED_CONTROL,
            speed=30.*constants.METERS_TO_VIS, 
            fine_behind=config.FINE_BEHIND_R, 
            fence_sigmoid=config.FENCE_SIGMOID, 
            car_control_bounds=constants.CAR_CONTROL_BOUNDS):
        """
        Define reward functions (tactical, and strategic value and
        hierarchical reward if applicable) given the input paremeters.
        Arguments:
         - world: world in which this reward is evaluated.
         - other_car_trajs: trajectories of the other cars.
         - other_truck_trajs: trajectories of the other trucks.
         - w_*: reward weights, see constants.py for descriptions. For weights
              corresponding to multiple objects (lanes, fences, other_car_trajs),
              the argument must be a list of weights corresponding to
              those objects in the order they appear in world.
         - speed: goal speed
         - fine_behind: if True, no penalty for being behind the other car
         - fence_sigmoid: if True, use sigmoid reward at edges of road.
              otherwise, use Gaussian shape.
         - car_control_bounds: bounds for the car controls
         - strategic_value_mat_name: name of MATLAB file containing data for
              the strategic value function. If None, only use tactical reward.
         """

        self.world = world
        self.other_car_trajs = other_car_trajs
        self.other_truck_trajs = other_truck_trajs
        if w_lanes is None:
            self.w_lanes = [config.W_LANES for _ in self.world.lanes]
        else:
            self.w_lanes = w_lanes
        if w_fences is None:
            self.w_fences = [config.W_FENCES for _ in self.world.fences]
        else:
            self.w_fences = w_fences
        self.w_speed = w_speed
        if w_other_car_trajs is None:
            self.w_other_car_trajs = [config.W_OTHER_CAR_TRAJS for _ in other_car_trajs]
        else:
            self.w_other_car_trajs = w_other_car_trajs
        if w_other_truck_trajs is None:
            self.w_other_truck_trajs = [config.W_OTHER_TRUCK_TRAJS for _ in other_truck_trajs]
        else:
            self.w_other_truck_trajs = w_other_truck_trajs
        self.w_behind = w_behind
        self.w_control = w_control
        self.w_bounded_control = w_bounded_control
        self.speed = speed
        self.fine_behind = fine_behind
        self.fence_sigmoid = fence_sigmoid
        self.car_control_bounds = car_control_bounds
        self.steering_bound = self.car_control_bounds[0][1]
        self.acceleration_bound = self.car_control_bounds[1][1]

        # reward definitions
        self.state_reward_np = self.get_state_reward(fw=np)
        self.state_reward_th = self.get_state_reward(fw=tt)
        self.control_reward_np = self.get_control_reward(fw=np)
        self.control_reward_th = self.get_control_reward(fw=tt)
        self.reward_np = self.state_reward_np + self.control_reward_np
        self.reward_th = self.state_reward_th + self.control_reward_th

    def get_config(self):
        """Return JSON object describing the parameters of this reward."""
        return {
            'w_lanes': self.w_lanes,
            'w_fences': self.w_fences,
            'w_speed': self.w_speed,
            'w_other_car_trajs': self.w_other_car_trajs,
            'w_other_truck_trajs': self.w_other_truck_trajs,
            'w_behind': self.w_behind,
            'w_control': self.w_control,
            'w_bounded_control': self.w_bounded_control,
            'speed': self.speed,
            'fine_behind': self.fine_behind,
            'fence_sigmoid': self.fence_sigmoid,
            'car_control_bounds': self.car_control_bounds,
            'steering_bound': self.steering_bound,
            'acceleration_bound': self.acceleration_bound
            }

    def state_rewards(self, fw):
        """Compute the individual state rewards and return them as a dictionary
        with keys that describe the rewards."""
        rewards = {}
        state_r = feature.feature(lambda t, x, u: 0.0)
        for i, (lane, w_lane) in enumerate(zip(self.world.lanes, self.w_lanes)):
            rewards['lane gaussian ' + str(i)] = w_lane * lane.gaussian(fw=fw)
        for i, (fence, w_fence) in enumerate(zip(self.world.fences, self.w_fences)):
            if self.fence_sigmoid: # sigmoid fence reward
                rewards['fence sigmoid ' + str(i)] = w_fence * fence.sigmoid(fw=fw)
            else: # gaussian-shaped fence reward
                rewards['fence gaussian ' + str(i)] = w_fence * fence.gaussian(fw=fw)
        if self.speed is not None:
            rewards['speed'] = self.w_speed * feature.speed(self.speed)
        for i, (other_car_traj, w_other_car_traj) in enumerate(zip(self.other_car_trajs, self.w_other_car_trajs)):
            if self.fine_behind:
                rewards['other traj gaussian ' + str(i)] = (w_other_car_traj * 
                    other_car_traj.gaussian(fw, length=.14, width=.03))
            else:
                rewards['other traj gaussian ' + str(i)] = (w_other_car_traj * 
                    other_car_traj.gaussian(fw, length=.14, width=.03))
                rewards['other traj not behind ' + str(i)] = other_car_traj.not_behind(
                    fw, self.w_behind)
        for i, (other_truck_traj, w_other_truck_traj) in enumerate(zip(self.other_truck_trajs, self.w_other_truck_trajs)):
            rewards['other truck sigmoid ' + str(i)] = (w_other_truck_traj *
                    other_truck_traj.sigmoid(fw))
        return rewards

    def get_state_reward(self, fw):
        """Compute the state reward."""
        state_r = feature.feature(lambda t, x, u: 0.0)
        for lane, w_lane in zip(self.world.lanes, self.w_lanes):
            state_r += w_lane * lane.gaussian(fw=fw)
        for fence, w_fence in zip(self.world.fences, self.w_fences):
            if self.fence_sigmoid: # sigmoid fence reward
                state_r += w_fence * fence.sigmoid(fw=fw)
            else: # gaussian-shaped fence reward
                state_r += w_fence * fence.gaussian(fw=fw)
        if self.speed is not None:
            state_r += self.w_speed * feature.speed(self.speed)
        for other_traj, w_other_traj in zip(self.other_car_trajs, self.w_other_car_trajs):
            if self.fine_behind:
                state_r += (w_other_traj * 
                    other_traj.gaussian(fw, length=.14, width=.03))
            else:
                state_r += (w_other_traj * 
                    other_traj.gaussian(fw, length=.14, width=.03) + 
                    other_traj.not_behind(fw, self.w_behind))
        for other_truck_traj, w_other_truck_traj in zip(self.other_truck_trajs, self.w_other_truck_trajs):
            state_r += (w_other_truck_traj *
                    other_truck_traj.sigmoid(fw))
        return state_r

    def get_control_reward(self, fw):
        """Compute the control reward."""
        control_r = (self.w_control * feature.control())
        bounded_control_r = (self.w_bounded_control *
            feature.bounded_control(fw, self.car_control_bounds))
        return control_r + bounded_control_r


def simple_reward(world, other_car_trajs, speed):
    w_lanes = [1.0 for _ in world.lanes]
    w_lanes[0] = 10.0
    return Reward(world, other_car_trajs, w_lanes=w_lanes, speed=speed, 
        fence_sigmoid=False)

