from decimal import Decimal
import pdb
import pprint
import sys

import numpy as np
import theano as th

import car
import config
import constants
import dynamics
import lane
import projection
import reward
from simulator import Simulator
from strategic_value import StrategicValue
import utils

class World(object):
    def __init__(self, name, dt, cars, main_robot_car, main_human_car, lanes, 
            roads, fences, objects=[], notices=[], feed_u=None, interaction_data=None):
        self.name = name
        self.cars = cars
        self.main_robot_car = main_robot_car
        self.main_human_car = main_human_car
        self.robot_cars = [c for c in self.cars if c.is_robot]
        user_controlled_cars = [c for c in self.cars if c.is_user_controlled]
        assert(len(user_controlled_cars) <= 1) # allow at most 1 user controlled car
        if len(user_controlled_cars) > 0:
            self.user_controlled_car = user_controlled_cars[0]
        else:
            self.user_controlled_car = None
        self.follower_cars = [c for c in self.cars if c.is_follower]
        self.lanes = lanes
        self.roads = roads
        self.fences = fences
        self.objects = objects
        self.notices = notices # show warnings when conditions are met.
        # simulates the dynamics and car movements
        self.simulator = Simulator(self, dt=dt, feed_u=feed_u, 
                interaction_data=interaction_data)

    def get_config(self):
        """Return JSON object describing the parameters of this experiment."""
        config_data = {
        'world':
            {
                'cars': {},
                'main_robot_car': str(self.main_robot_car),
                'main_human_car': str(self.main_human_car),
                'lanes': [str(x) for x in self.lanes],
                'roads': [str(x) for x in self.roads],
                'fences': [str(x) for x in self.fences]
            },
        'config':
            {
                'OPT_TIMEOUT': config.OPT_TIMEOUT,
                'NESTEDMAX_MAXITER_INNER': config.NESTEDMAX_MAXITER_INNER,
                'HORIZON': config.HORIZON,
                'STRATEGIC_VALUE_4D_DATA_DIR': config.STRATEGIC_VALUE_4D_DATA_DIR,
                'STRATEGIC_VALUE_3D_DATA_DIR': config.STRATEGIC_VALUE_3D_DATA_DIR,
                'STRAT_DIM': config.STRAT_DIM,
                'STRATEGIC_VALUE_SCALE': config.STRATEGIC_VALUE_SCALE,
                'USE_SECOND_ORDER': config.USE_SECOND_ORDER,
                'HUMAN_BETA': config.HUMAN_BETA,
                'INIT_PLAN_SCHEME': config.INIT_PLAN_SCHEME
            }
        }
        # Config for each car
        for c in self.cars:
            car_config = {
                'dt': c.dt,
                'bounds': c.bounds,
                'name': c.name,
                'horizon': c.horizon,
                'is_robot': c.is_robot,
                'is_user_controlled': c.is_user_controlled,
                'is_follower': c.is_follower
            }
            config_data['world']['cars'][str(c)] = car_config
        # Config for reward of each car
        rewards = {}
        reward_names = ['reward', 'reward_h', 'reward_r', 'strat_val', 'strat_val_h', 'strat_val_r']
        for c in self.cars:
            rewards[str(c)] = {}
            for reward_name in reward_names:
                if hasattr(c, reward_name) and eval('c.' + reward_name) is not None:
                    rewards[str(c)][reward_name] = eval('c.' + reward_name).get_config()
        config_data['rewards'] = rewards
        return config_data

def get_initial_states(scenario):
    initial_speed_r = constants.METERS_TO_VIS*32.0
    # initial_speed_h = initial_speed_r
    initial_speed_h = constants.METERS_TO_VIS*32.0
    if scenario == 'far_overtaking':
        x0_r = np.array([0.0, 0.0, np.pi/2., initial_speed_r])
        x0_h = np.array([0.0, 1.0, np.pi/2., initial_speed_h])
    elif scenario == 'overtaking':
        x0_r = np.array([0.0, 0.0, np.pi/2., initial_speed_r])
        x0_h = np.array([0.0, 0.7, np.pi/2., initial_speed_h])
    elif scenario == 'easy_merging':
        x0_r = np.array([constants.LEFT_LANE_CENTER + constants.LANE_WIDTH_VIS, 
            0.35, np.pi/2., initial_speed_r])
        x0_h = np.array([0.0, 0.0, np.pi/2., initial_speed_h])
    elif scenario == 'hard_merging':
        x0_r = np.array([constants.LEFT_LANE_CENTER + constants.LANE_WIDTH_VIS, 
            0.0, np.pi/2., initial_speed_r])
        x0_h = np.array([0.0, 0.3, np.pi/2., initial_speed_h])
    elif scenario == 'truck_cut_in_human_in_front':
        x0_r = np.array([0.0, 0.0, np.pi/2., config.INITIAL_SPEED_R])
        x0_h = np.array([0.0, 0.7, np.pi/2., initial_speed_h])
        x0_t = np.array([constants.RIGHT_LANE_CENTER, 0.7 + config.FRONT_Y_REL, np.pi/2., constants.TRUCK_CONSTANT_SPEED])
        return x0_r, x0_h, x0_t
    elif scenario == 'truck_cut_in_robot_in_front':
        x0_r = np.array([0.0, 0.7, np.pi/2., initial_speed_r])
        x0_h = np.array([0.0, 0.0, np.pi/2., initial_speed_h])
        x0_t = np.array([constants.RIGHT_LANE_CENTER, 0.7 + config.FRONT_Y_REL, np.pi/2., constants.TRUCK_CONSTANT_SPEED])
        return x0_r, x0_h, x0_t
    elif scenario == 'truck_cut_in_hard_merge':
        y0_h = 0.
        y0_r = y0_h - 5. * constants.METERS_TO_VIS
        y0_t = y0_h + config.FRONT_Y_REL
        v0_h = constants.METERS_TO_VIS * 30.
        v0_r = config.INITIAL_SPEED_R
        v0_t = constants.TRUCK_CONSTANT_SPEED
        # states
        x0_r = np.array([constants.RIGHT_LANE_CENTER, y0_r, np.pi/2., v0_r])
        x0_h = np.array([0.0, y0_h, np.pi/2., v0_h])
        x0_t = np.array([constants.RIGHT_LANE_CENTER, y0_t, np.pi/2., v0_t])
        return x0_r, x0_h, x0_t
    # elif scenario == 'truck_cut_in_hard_merge_human_lets_robot_in':
    #     x0_r = np.array([0.13, 40. * constants.METERS_TO_VIS, np.pi/2., constants.METERS_TO_VIS * 39.])
    #     x0_h = np.array([0.0, 50. * constants.METERS_TO_VIS, np.pi/2., constants.METERS_TO_VIS * 30.])
    #     x0_t = np.array([constants.RIGHT_LANE_CENTER, 70. * constants.METERS_TO_VIS, np.pi/2., constants.TRUCK_CONSTANT_SPEED])
    #     return x0_r, x0_h, x0_t
    # elif scenario == 'truck_cut_in_hard_merge_human_cuts_off_robot':
    #     x0_r = np.array([0.13, 40. * constants.METERS_TO_VIS, np.pi/2., constants.METERS_TO_VIS * 38.])
    #     x0_h = np.array([0.0, 50. * constants.METERS_TO_VIS, np.pi/2., constants.METERS_TO_VIS * 30.])
    #     x0_t = np.array([constants.RIGHT_LANE_CENTER, 70. * constants.METERS_TO_VIS, np.pi/2., constants.TRUCK_CONSTANT_SPEED])
    #     return x0_r, x0_h, x0_t
    else:
        print 'Error: unknown scenario: "{0}"'.format(scenario)
        sys.exit()
    return x0_r, x0_h

def world_test(init_planner=True):
    # lanes
    center_lane = lane.StraightLane([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS)
    left_lane = center_lane.shifted(1)
    right_lane = center_lane.shifted(-1)
    lanes = [center_lane, left_lane, right_lane]
    roads = []
    # fences
    fences = [center_lane.shifted(2), center_lane.shifted(-2)]
    # dynamics
    dyn = dynamics.CarDynamics
    # cars
    x0_h = np.array([-constants.LANE_WIDTH_VIS, 0., np.pi/2., 0.3])
    human_car = car.UserControlledCar(x0_h, constants.DT, dyn, 
        constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
        color=constants.COLOR_H, name=constants.NAME_H)
    x0_r = np.array([0.0, 0.5, np.pi/2., 0.3])
    robot_car = car.SimpleOptimizerCar(x0_r, constants.DT, dyn, 
        constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
        color=constants.COLOR_R, name=constants.NAME_R)
    cars = [robot_car, human_car]

    name = 'world_test'
    world = World(name, constants.DT, cars, robot_car, human_car, lanes, roads, 
        fences)

    # rewards
    robot_car.reward = reward.simple_reward(world, [human_car.traj_linear], 
        speed=0.5)

    # initialize planners
    for c in world.robot_cars:
        c.init_planner()

    return world


def world_highway(initial_states='overtaking', 
        interaction_data=None, init_planner=True):
    # If very long horizon, increase bracket depth in Theano compilation to avoid
    # "fatal error: bracket nesting level exceeded maximum of 256."
    if config.HORIZON > 10:
        th.config.gcc.cxxflags = '-fbracket-depth=1024'

    # lanes
    left_lane = lane.StraightLane([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS)
    right_lane = left_lane.shifted(-1)
    lanes = [left_lane, right_lane]
    # roads
    roads = [left_lane]
    # fences (road boundaries)
    right_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=1)
    left_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=-1)
    fences = [right_fence.shifted(-1.5), left_fence.shifted(0.5)]
    # dynamics
    dyn = dynamics.CarDynamics
    # asynchronous setting
    config.ASYNCHRONOUS = False

    # MATLAB file setup
    fine_behind_h = config.FINE_BEHIND_H
    fine_behind_r = config.FINE_BEHIND_R
    human_beta = config.HUMAN_BETA
    assert(config.STRAT_DIM == 3 or config.STRAT_DIM == 4)
    if config.STRAT_DIM == 3:
        strat_val_data_dir = config.STRATEGIC_VALUE_3D_DATA_DIR
    elif config.STRAT_DIM == 4:
        strat_val_data_dir = config.STRATEGIC_VALUE_4D_DATA_DIR
    if fine_behind_h == True:
        if human_beta is None:
            print('Not using strategic value.')
        elif human_beta == float('inf'): # then rational human (= deterministic).
            mat_name = strat_val_data_dir + 'DSG_fine_det.mat'
        else:
            beta_str = '%.2E' % Decimal(config.HUMAN_BETA)
            mat_name = strat_val_data_dir + 'beta_{0}/DSG_fine_beta_{0}.mat'.format(
                beta_str)
        # elif human_beta == 1:
        #     mat_name = strat_val_data_dir + 'DSG_fine_beta1.mat'
        # else:
        #     print('Unkown human beta.')
        #     sys.exit()
    else:
        if human_beta is None:
            print('Not using strategic value.')
        elif human_beta == float('inf'): # then rational human (= deterministic).
            mat_name = strat_val_data_dir + 'DSG_not_fine_det.mat'
        else:
            beta_str = '%.2E' % Decimal(config.HUMAN_BETA)
            mat_name = strat_val_data_dir + 'beta_{0}/DSG_fine_beta_{0}.mat'.format(
                beta_str)
        # elif human_beta == 1:
        #     mat_name = strat_val_data_dir + 'DSG_not_fine_beta1.mat'
        # else:
        #     print('Unkown human beta.')
        #     sys.exit()

    # Strategic state projection
    if config.STRAT_DIM == 3:
        proj = projection.ProjectionStrategicValue3D()
        # proj_th = utils.tact_to_strat_proj_3d_th
        # proj_np = utils.tact_to_strat_proj_3d_np

    elif config.STRAT_DIM == 4:
        proj = projection.ProjectionStrategicValue4D()
        # proj_th = utils.tact_to_strat_proj_4d_th
        # proj_np = utils.tact_to_strat_proj_4d_np

    # Initial states
    x0_r, x0_h = get_initial_states(initial_states)

    # Robot car setup
    ref_speed_r = constants.METERS_TO_VIS*35.0
    initial_speed_r = constants.METERS_TO_VIS*32.0
    if config.ROBOT_CAR == 'car.HierarchicalCar' or config.ROBOT_CAR == 'car.PredictReactHierarchicalCar':
        car_class = eval(config.ROBOT_CAR)
        robot_car = car_class(x0_r, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_R, name=constants.NAME_R,
            mat_name=mat_name, use_second_order=config.USE_SECOND_ORDER,
            proj=proj, strat_dim=config.STRAT_DIM)
    elif config.ROBOT_CAR == 'car.NestedCar' or config.ROBOT_CAR == 'car.PredictReactCar':
        car_class = eval(config.ROBOT_CAR)
        robot_car = car_class(x0_r, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_R, name=constants.NAME_R,
            use_second_order=config.USE_SECOND_ORDER)
    else:
        print('"{0}" is currently an unsupported robot car type'.format(config.ROBOT_CAR))
        sys.exit()

    # Human car setup
    # ref_speed_h = x0_h[3]
    ref_speed_h = constants.METERS_TO_VIS * 32.0
    human_car = eval(config.HUMAN_CAR)(x0_h, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_H, name=constants.NAME_H)
    
    # information structure
    robot_car.human = human_car # robot creates its own traj for human
    if human_car.is_follower: # give follower car access to the robot car
        human_car.robot = robot_car
    human_car.traj_r = robot_car.traj # human knows the robot traj
    
    # world setup
    cars = [robot_car, human_car]
    name = 'world_hierarchical_overtaking'
    world = World(name, constants.DT, cars, robot_car, human_car, lanes, roads, 
                fences, interaction_data=interaction_data)

    # rewards
    w_lanes = [4., 1.]
    w_control = -0.1
    w_bounded_control_h = -50.0 # bounded control weight for human
    w_bounded_control_r = -50.0 # bounded control weight for robot
    # Rewards and strategic value modeled by the robot 
    # (for both human and robot, respectively)
    if config.R_BELIEF_H_KNOWS_TRAJ_R: # robot believes human knows robot trajectory
        robot_r_h_traj = robot_car.traj
    else: # robot believes human doesn't know robot trajectory
        robot_r_h_traj = robot_car.traj_linear
    robot_r_h = reward.Reward(world, [robot_r_h_traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_h,
            speed=ref_speed_h,
            fine_behind=fine_behind_h)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    robot_r_r = reward.Reward(world, [robot_car.traj_h],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_r,
            speed=ref_speed_r,
            fine_behind=fine_behind_r)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    robot_car.reward = robot_r_r
    robot_car.reward_h = robot_r_h
    if config.PREDICT_HUMAN_IGNORES_ROBOT:
        # Reward for a human that ignores the existence of the robot.
        robot_r_h_ignore_robot = reward.Reward(world, other_car_trajs=[],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_h,
            speed=ref_speed_h,
            fine_behind=fine_behind_h)
        robot_car.reward_h_ignore_robot = robot_r_h_ignore_robot
    if config.ROBOT_CAR == 'car.HierarchicalCar' or config.ROBOT_CAR == 'car.PredictReactHierarchicalCar':
        # Robot's model of the human strategic value
        robot_strat_val_h = StrategicValue(robot_car.traj, robot_car.traj_h,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        # Robot's strategic value
        # TODO: just trying out human_car.traj to debug heatmap vis
        # robot_strat_val = StrategicValue(robot_car.traj, human_car.traj,
        #     proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
        #     min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        robot_strat_val = StrategicValue(robot_car.traj, robot_car.traj_h,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        robot_car.strat_val = robot_strat_val
        robot_car.strat_val_h = robot_strat_val_h

    # Rewards and strategic value modeled by the human WHEN SIMULATED 
    # (for both human and robot, respectively)
    human_r_h = reward.Reward(world, [human_car.traj_r],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_h,
            speed=ref_speed_h,
            fine_behind=fine_behind_h)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    human_r_r = reward.Reward(world, [human_car.traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_r,
            speed=ref_speed_r,
            fine_behind=fine_behind_r)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    human_car.reward = human_r_h
    human_car.reward_r = human_r_r
    if config.ROBOT_CAR == 'car.HierarchicalCar' or config.ROBOT_CAR == 'car.PredictReactHierarchicalCar':
        # Human's strategic value
        human_strat_val = StrategicValue(human_car.traj_r, human_car.traj,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        # Human's model of the robot strategic value
        human_strat_val_r = StrategicValue(human_car.traj_r, human_car.traj,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        human_car.strat_val = human_strat_val
        human_car.strat_val_r = human_strat_val_r

    # set min and max strategic values
    # config.MIN_STRAT_VAL = config.STRATEGIC_VALUE_SCALE * min(
    #         [min(robot_strat_val_h.vH_grid.flatten()), min(robot_strat_val_h.vR_grid.flatten()),
    #         min(robot_strat_val.vH_grid.flatten()), min(robot_strat_val.vR_grid.flatten()),
    #         min(human_strat_val.vH_grid.flatten()), min(human_strat_val.vR_grid.flatten()),
    #         min(human_strat_val_r.vH_grid.flatten()), min(human_strat_val_r.vR_grid.flatten())])
    # config.MAX_STRAT_VAL = config.STRATEGIC_VALUE_SCALE * max(
    #         [max(robot_strat_val_h.vH_grid.flatten()), max(robot_strat_val_h.vR_grid.flatten()),
    #         max(robot_strat_val.vH_grid.flatten()), max(robot_strat_val.vR_grid.flatten()),
    #         max(human_strat_val.vH_grid.flatten()), max(human_strat_val.vR_grid.flatten()),
    #         max(human_strat_val_r.vH_grid.flatten()), max(human_strat_val_r.vR_grid.flatten())])
    
    # print the configuration
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(world.get_config())

    # initialize planners
    if init_planner:
        print('Initializing planners.')
        for c in world.cars:
            if hasattr(c, 'init_planner'):
                print 'Initializing planner for ' + c.name
                c.init_planner(config.INIT_PLAN_SCHEME[c.name])
                print '\n'

    return world


def world_highway_truck_cut_in(initial_states='truck_cut_in_far_overtaking',
        interaction_data=None, init_planner=True):
    # If very long horizon, increase bracket depth in Theano compilation to avoid
    # "fatal error: bracket nesting level exceeded maximum of 256."
    if config.HORIZON > 10:
        th.config.gcc.cxxflags = '-fbracket-depth=1024'

    # lanes
    left_lane = lane.StraightLane([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS)
    right_lane = left_lane.shifted(-1)
    lanes = [left_lane, right_lane]
    # roads
    roads = [left_lane]
    # fences (road boundaries)
    right_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=1)
    left_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=-1)
    fences = [right_fence.shifted(-1.5), left_fence.shifted(0.5)]
    # dynamics
    dyn = dynamics.CarDynamics
    # asynchronous setting
    config.ASYNCHRONOUS = False

    # MATLAB file setup
    fine_behind_h = config.FINE_BEHIND_H
    fine_behind_r = config.FINE_BEHIND_R
    human_beta = config.HUMAN_BETA
    strat_val_data_dir = config.TRUCK_CUT_IN_STRATEGIC_VALUE_DATA_DIR
    if fine_behind_h == True:
        if human_beta is None:
            print('Not using strategic value.')
        elif human_beta == float('inf'): # then rational human (= deterministic).
            mat_name = strat_val_data_dir + 'DSG_fine_det.mat'
        else:
            beta_str = '%.2E' % Decimal(config.HUMAN_BETA)
            mat_name = strat_val_data_dir + 'beta_{0}/DSG_fine_beta_{0}.mat'.format(
                beta_str)
    else:
        if human_beta is None:
            print('Not using strategic value.')
        elif human_beta == float('inf'): # then rational human (= deterministic).
            mat_name = strat_val_data_dir + 'DSG_not_fine_det.mat'
        else:
            beta_str = '%.2E' % Decimal(config.HUMAN_BETA)
            mat_name = strat_val_data_dir + 'beta_{0}/DSG_fine_beta_{0}.mat'.format(
                beta_str)

    # Strategic state projection (use strategic grid dimension to get the correct
    # projection)
    proj = eval('projection.ProjectionTruckCutInStrategicValue{0}D'.format(config.STRAT_DIM))()

    # Initial states
    x0_r, x0_h, x0_t = get_initial_states(initial_states)

    # Robot car setup
    ref_speed_r = constants.METERS_TO_VIS * 35.0
    if config.ROBOT_CAR == 'car.HierarchicalCar':
        robot_car = car.HierarchicalCar(x0_r, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_R, name=constants.NAME_R,
            mat_name=mat_name, use_second_order=config.USE_SECOND_ORDER,
            proj=proj, strat_dim=config.STRAT_DIM)
    elif config.ROBOT_CAR == 'car.NestedCar':
        robot_car = car.NestedCar(x0_r, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_R, name=constants.NAME_R,
            use_second_order=config.USE_SECOND_ORDER)
    elif config.ROBOT_CAR == 'car.PredictReactCar':
        robot_car = car.PredictReactCar(x0_r, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_R, name=constants.NAME_R)
    else:
        print('"{0}" is currently an unsupported robot car type'.format(config.ROBOT_CAR))
        sys.exit()

    # Human car setup
    ref_speed_h = constants.METERS_TO_VIS * 32. # x0_h[3]
    human_car = eval(config.HUMAN_CAR)(x0_h, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_H, name=constants.NAME_H)
    
    # Truck setup
    truck = car.Truck(x0_t, constants.DT, dyn, 
            constants.CAR_CONTROL_BOUNDS, horizon=config.HORIZON, 
            color=constants.COLOR_TRUCK, name=constants.NAME_TRUCK)
    

    # Information structure
    robot_car.human = human_car # robot creates its own traj for human
    if human_car.is_follower: # give follower car access to the robot car
        human_car.robot = robot_car
    human_car.traj_r = robot_car.traj # human knows the robot traj
    robot_car.truck = truck
    human_car.truck = truck
    
    # world setup
    cars = [robot_car, human_car, truck]
    name = 'world_highway_truck_cut_in'
    world = World(name, constants.DT, cars, robot_car, human_car, lanes, roads, 
                fences, interaction_data=interaction_data)

    # rewards
    w_lanes = [4., 1.]
    w_control = -0.1
    w_bounded_control_h = -50.0 # bounded control weight for human
    w_bounded_control_r = -50.0 # bounded control weight for robot
    # Rewards and strategic value modeled by the robot 
    # (for both human and robot, respectively)
    if config.R_BELIEF_H_KNOWS_TRAJ_R: # robot believes human knows robot trajectory
        robot_r_h_traj = robot_car.traj
    else: # robot believes human doesn't know robot trajectory
        robot_r_h_traj = robot_car.traj_linear
    robot_r_h = reward.Reward(world, [robot_r_h_traj],
            other_truck_trajs=[truck.traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_h,
            speed=ref_speed_h,
            fine_behind=fine_behind_h)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    robot_r_r = reward.Reward(world, [robot_car.traj_h],
            other_truck_trajs=[truck.traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_r,
            speed=ref_speed_r,
            fine_behind=fine_behind_r)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    robot_car.reward = robot_r_r
    robot_car.reward_h = robot_r_h
    if config.ROBOT_CAR == 'car.HierarchicalCar':
        # Robot's model of the human strategic value
        robot_strat_val_h = StrategicValue(robot_car.traj, robot_car.traj_h,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL, 
            traj_truck=truck.traj)
        # Robot's strategic value
        # TODO: just trying out human_car.traj to debug heatmap vis
        # robot_strat_val = StrategicValue(robot_car.traj, human_car.traj,
        #     proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
        #     min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL)
        robot_strat_val = StrategicValue(robot_car.traj, robot_car.traj_h,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL, 
            traj_truck=truck.traj)
        robot_car.strat_val = robot_strat_val
        robot_car.strat_val_h = robot_strat_val_h

    # Rewards and strategic value modeled by the human WHEN SIMULATED 
    # (for both human and robot, respectively)
    human_r_h = reward.Reward(world, [human_car.traj_r],
            other_truck_trajs=[truck.traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_h,
            speed=ref_speed_h,
            fine_behind=fine_behind_h)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    human_r_r = reward.Reward(world, [human_car.traj],
            other_truck_trajs=[truck.traj],
            w_lanes=w_lanes,
            w_control=w_control,
            w_bounded_control=w_bounded_control_r,
            speed=ref_speed_r,
            fine_behind=fine_behind_r)#,
            # strategic_value_mat_name=mat_name, robot_car=robot_car,
            # proj_np=proj_np, proj_th=proj_th)
    human_car.reward = human_r_h
    human_car.reward_r = human_r_r
    if config.ROBOT_CAR == 'car.HierarchicalCar':
        # Human's strategic value
        human_strat_val = StrategicValue(human_car.traj_r, human_car.traj,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL, 
            traj_truck=truck.traj)
        # Human's model of the robot strategic value
        human_strat_val_r = StrategicValue(human_car.traj_r, human_car.traj,
            proj, mat_name, config.STRAT_DIM, config.STRATEGIC_VALUE_SCALE,
            min_val=config.MIN_STRAT_VAL, max_val=config.MAX_STRAT_VAL, 
            traj_truck=truck.traj)
        human_car.strat_val = human_strat_val
        human_car.strat_val_r = human_strat_val_r

        # set min and max strategic values
        config.MIN_STRAT_VAL = config.STRATEGIC_VALUE_SCALE * min(
                [min(robot_strat_val_h.vH_grid.flatten()), min(robot_strat_val_h.vR_grid.flatten()),
                min(robot_strat_val.vH_grid.flatten()), min(robot_strat_val.vR_grid.flatten()),
                min(human_strat_val.vH_grid.flatten()), min(human_strat_val.vR_grid.flatten()),
                min(human_strat_val_r.vH_grid.flatten()), min(human_strat_val_r.vR_grid.flatten())])
        config.MAX_STRAT_VAL = config.STRATEGIC_VALUE_SCALE * max(
                [max(robot_strat_val_h.vH_grid.flatten()), max(robot_strat_val_h.vR_grid.flatten()),
                max(robot_strat_val.vH_grid.flatten()), max(robot_strat_val.vR_grid.flatten()),
                max(human_strat_val.vH_grid.flatten()), max(human_strat_val.vR_grid.flatten()),
                max(human_strat_val_r.vH_grid.flatten()), max(human_strat_val_r.vR_grid.flatten())])

    # print the configuration
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(world.get_config())

    # initialize planners
    if init_planner:
        print('Initializing planners.')
        for c in world.cars:
            if hasattr(c, 'init_planner'):
                print 'Initializing planner for ' + c.name
                c.init_planner(config.INIT_PLAN_SCHEME[c.name])
                print '\n'

    return world


def standard_2lane_road():
    # lanes
    left_lane = lane.StraightLane([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS)
    right_lane = left_lane.shifted(-1)
    lanes = [left_lane, right_lane]
    # roads
    roads = [left_lane]
    # fences (road boundaries)
    right_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=1)
    left_fence = lane.Fence([0., -1.], [0., 1.], constants.LANE_WIDTH_VIS, side=-1)
    fences = [right_fence.shifted(-1.5), left_fence.shifted(0.5)]
    return lanes, roads, fences
