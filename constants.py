import numpy as np

### Directory structure
DATA_DIR = 'assets/data/'
INTERACTION_FRAME_DIR = 'assets/interaction_frames/' # contains frames of interaction
MAT_DATA_DIR = DATA_DIR + 'mat/' # MATLAB files
# 4D strategic value
STRATEGIC_VALUE_4D_OFFGRID_PROJECTION_DATA_DIR = MAT_DATA_DIR + 'strategic_value_4d_offgrid_projection/'
STRATEGIC_VALUE_4D_OFFGRID_FREEZE_DATA_DIR = MAT_DATA_DIR + 'strategic_value_4d_offgrid_freeze/'
STRATEGIC_VALUE_4D_OFFGRID_FREEZE_UNWEIGHTED_DATA_DIR = MAT_DATA_DIR + 'strategic_value_4d_offgrid_freeze_unweighted/'
STRATEGIC_VALUE_4D_OFFGRID_PROJECTION_VREL_DATA_DIR = MAT_DATA_DIR + 'strategic_value_4d_offgrid_projection_vrel/'
STRATEGIC_VALUE_4D_TEST = MAT_DATA_DIR + 'strategic_value_4d_test/'
# Truck cut in scenario strategic value
## uses relative velocity reward
# shorter y_rel (3 in vis units)
TRUCK_CUT_IN_STRATEGIC_VALUE_5D_OFFGRID_PROJECTION_DATA_DIR_VREL = MAT_DATA_DIR + 'truck_cut_in_strategic_value_5d_offgrid_projection_vrel/'
# longer y_rel (5 in vis units)
TRUCK_CUT_IN_STRATEGIC_VALUE_5D_OFFGRID_PROJECTION_LONGER_YREL_DATA_DIR_VREL = MAT_DATA_DIR + 'truck_cut_in_strategic_value_5d_offgrid_projection_longer_yrel_vrel/'
## uses absolute velocity reward
TRUCK_CUT_IN_STRATEGIC_VALUE_5D_OFFGRID_PROJECTION_LONGER_YREL_DATA_DIR_VABS = MAT_DATA_DIR + 'truck_cut_in_strategic_value_5d_offgrid_projection_longer_yrel_vabs/'
# 6D
TRUCK_CUT_IN_STRATEGIC_VALUE_6D_OFFGRID_PROJECTION_SHORTER_YREL_DATA_DIR_VABS = MAT_DATA_DIR + 'truck_cut_in_strategic_value_6d_offgrid_projection_shorter_yrel_vabs/'

IMAGE_DIR = 'assets/img/'
SCREENSHOT_DIR = 'assets/screenshots/'
INTERACTION_DATA_DIR = 'assets/data/interaction_data/'
TIME_PROFILE_DIR = 'assets/data/time_profile/'

### Visualization
PAUSE_EVERY_N = None # pause the program every n iterations of control_loop
# Options for which heatmap to visualize: robot's strategic value, human's
# strategic value, robot's tactical reward, human's tactical reward
HEATMAP_OPTIONS = ['r_strat', 'h_strat', 'r_tact', 'h_tact']

### World measurements
LANE_WIDTH_VIS = 0.13 # lane width in vis units
LANE_WIDTH_METERS = 3.7 # lane width in meters
METERS_TO_VIS = LANE_WIDTH_VIS / LANE_WIDTH_METERS # meters * METERS_TO_VIS ==> vis units
LEFT_LANE_CENTER = 0.0 # x position of center of left lane
RIGHT_LANE_CENTER = LEFT_LANE_CENTER + LANE_WIDTH_VIS

### Cars
NAME_H = 'human'
NAME_R = 'robot'
NAME_TRUCK = 'truck'
COLOR_H = 'white'
COLOR_R = 'yellow'
COLOR_TRUCK = 'truck'
WHEELBASE = 3
# Options for the type of the human car
HUMAN_CAR_OPTIONS = ['SimpleOptimizerCar', 'FollowerCar', 'UserControlledCar', 'MaintainSpeedCar', 'BadOptimizerCar']
# Options for the type of the robot car
ROBOT_CAR_OPTIONS = ['HierarchicalCar', 'NestedCar', 'SimpleOptimizerCar', 'PredictReactCar', 'PredictReactHierarchicalCar', 'IteratedBestResponseCar', 'ILQRCar']
# Physical dimensions of cars/trucks
CAR_LENGTH = 0.148 # length of car
CAR_WIDTH = 1.9 * METERS_TO_VIS # width of car
TRUCK_LENGTH = 0.6957 # length of trucks
#TRUCK_WIDTH = 1 * METERS_TO_VIS # width of truck.
TRUCK_WIDTH = 0.5 * METERS_TO_VIS # width of truck.


### Dynamics
FRICTION = 0.016745192307692 # from DSG toolbox; old friction value: 0.023
# [steering (rad), acceleration (m/s^2)]
# old car control bounds: [(-0.124, 0.124), (-2*0.0878, 0.0878)]
NO_BOUNDS = [(10, 10), (10, 10)]
CAR_CONTROL_BOUNDS = [(-3*0.13/3, 3*0.13/3), (-12*0.0878, 3 * 0.0878)] #
# Control bounds for human car in the hierarchical setup to get a numerically 
# stable algorithm. Temporary solution!
HIERARCHICAL_HUMAN_CONTROL_BOUNDS = [(-0.104, 0.104), (-0.0878, 0.0878)]
TRUCK_CONTROL_BOUNDS = [(-5*0.0206, 0.0206)] # m/s^2
# Options describing the initial states of the cars for different scenarios
INITIAL_STATE_OPTIONS = ['far_overtaking', 'overtaking', 'easy_merging', 'hard_merging', 'truck_cut_in_human_in_front', 'truck_cut_in_robot_in_front', 'truck_cut_in_hard_merge']
# Constant speed of the truck
TRUCK_CONSTANT_SPEED = METERS_TO_VIS * 26.8224 # corresponds to 60 mph

### Control
K_STEER = 6.5 # steering multiplier constant. # world7: 6.5, world7_test: 180.0 / math.pi
K_ACCELERATION = 3.09 # acceleration multiplier constant
K_BRAKE = -2.53 # conversion from steering control in visualization to OpenDS for the autonomous car
K_STEER_USER = 0.15 # steering multiplier constant for user. For OpenDS: 50.0
K_GAS_USER = 0.15 # gas multiplier constant for user
K_BRAKE_USER = 0.15 # brake multiplier constant for user

### Data dimensions
STATE_DIM = 4
CONTROL_DIM = 2
TRUCK_CONTROL_DIM = 1

### Planning
DT = 0.1 # control loop time step in synchronous mode
ANIMATION_DT = 1.0 / 120.0 # animation loop time step
# Schemes for how to initialize the car's plan when doing optimization.
# prev_opt: initialize to the optimal plan computed at the previous time step,
    # shifted by 1 index and with a zero control added at the end.
# lsr: initialize to max left steering, then no steering, then max right steering,
    # each with 0 acceleration.
INIT_PLAN_SCHEMES_OPTIONS = ['prev_opt', 'lsr', 'max_speed_prev_steer', 'maintain_speed_prev_steer', 'maintain_speed_lsr', 'maintain_speed_lsr_and_prev_opt']
# Dictionary mapping plan initialization schemes to the number of optimization
# loops for the robot and human, respectively.
INIT_PLAN_SCHEME_TO_NUM_OPTS_R = {'prev_opt': 1, 'lsr': 3, 'max_speed_prev_steer': 1, 'maintain_speed_prev_steer': 1, 'maintain_speed_lsr': 3, 'maintain_speed_lsr_and_prev_opt': 4}
INIT_PLAN_SCHEME_TO_NUM_OPTS_H = {'prev_opt': 1, 'lsr': 3, 'max_speed_prev_steer': 1, 'maintain_speed_prev_steer': 1, 'maintain_speed_lsr': 3, 'maintain_speed_lsr_and_prev_opt': 4}

### Rewards
LANE_REWARD_STDEV_h = 1 * LANE_WIDTH_VIS / 4. # standard deviation of lane Gaussian reward
LANE_REWARD_STDEV_r = 1.3 * LANE_WIDTH_VIS / 4. # standard deviation of lane Gaussian reward
BEHIND_REWARD_SLOPE = 1.0 / 0.01 # slope of reward for being behind the other car
STEER_REWARD_SCALING = 1.0 / CAR_CONTROL_BOUNDS[0][1]
ACCELERATION_REWARD_SCALING = 1.0 / CAR_CONTROL_BOUNDS[1][1]


# Fence reward
# Steepness of fence rewards. Fence reward is fenceRefCost when vehicle is 
# fenceRefFraction * config.laneW away from the fence.
FENCE_REF_COST = 0.1
FENCE_REF_FRACTION = 0.3
FENCE_REWARD_SCALE = np.log(1. / FENCE_REF_COST - 1) / (FENCE_REF_FRACTION * LANE_WIDTH_VIS)

# Truck proximity reward
# Distance between truck and car at which point they collide. Used for truck
# proximity reward
TRUCK_REWARD_WIDTH = CAR_WIDTH / 2. + TRUCK_WIDTH / 2. # x-direction
TRUCK_REWARD_LENGTH = CAR_LENGTH / 2. + TRUCK_LENGTH / 2. # y-direction
TRUCK_REWARD_SCALE = FENCE_REWARD_SCALE

# ### Reward weights from IRL
# W_IRL_LANES = 0.959 # stay in center of lane
# W_IRL_FENCES = -46.271 # stay on the road (i.e. away from fences on sides of road)
# W_IRL_SPEED = -9.015 # keep at goal speed
# W_IRL_ROAD = 8.531 # stay on road
# W_IRL_OTHER_TRAJS = -57.604 # stay away from other cars