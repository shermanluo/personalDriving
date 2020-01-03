"""Define configurable settings."""

import constants

### General configuration
EXTERNAL_WORLD = False
ASYNCHRONOUS = False
# The type of the "robot" an human" cars. Must be specified in the form 'car.CarClass'
# (where CarClass is a car class defined in car.py) because this string will be
# eval'd.
HUMAN_CAR = 'car.SimpleOptimizerCar'
ROBOT_CAR = 'car.HierarchicalCar'

### World setup
# Initial relative y-distance between the truck and the car in front (y_truck - y_front_car). 
# Only applicable for the truck cut-in scenarios.
FRONT_Y_REL = 2.
# Initial speed of the robot.
INITIAL_SPEED_R = constants.METERS_TO_VIS * 32.0

### Information structure
# if True, robot believes that human knows the robot trajectory. 
# Else, robot belieyves human doesn't know robot trajectory and uses a trajectory
# in which robot applies zero control
R_BELIEF_H_KNOWS_TRAJ_R = True
# If True, robot will predict that human's reward is independent of the robot's 
# trajectory (i.e. human ignores the robot).
PREDICT_HUMAN_IGNORES_ROBOT = False

### Optimization
OPT_TIMEOUT = 0.1 # max time for optimization (planning)
# max number of iterations in the inner optimization loop of the nested optimization
NESTEDMAX_MAXITER_INNER = 20

### Planning
HORIZON = 5
# Dictionary mapping from car name to its plan initialization scheme for its
# optimizer.
INIT_PLAN_SCHEME = {constants.NAME_H: 'prev_opt', constants.NAME_R: 'prev_opt', constants.NAME_TRUCK: 'None'}

### Hierarchical planning
# current 4D strategic value data directory
STRATEGIC_VALUE_4D_DATA_DIR = constants.STRATEGIC_VALUE_4D_OFFGRID_PROJECTION_VREL_DATA_DIR
# current 3D strategic value data directory
STRATEGIC_VALUE_3D_DATA_DIR = constants.MAT_DATA_DIR + 'strategic_value_3d_new/'
# current truck cut in scenario strategic value data directory
TRUCK_CUT_IN_STRATEGIC_VALUE_DATA_DIR = constants.TRUCK_CUT_IN_STRATEGIC_VALUE_6D_OFFGRID_PROJECTION_SHORTER_YREL_DATA_DIR_VABS

STRAT_DIM = 4 # dimension of strategic value
STRATEGIC_VALUE_SCALE = 5.0 # scaling for the strategic reward in the DSG
# if True, use Hessian for hierarchical optimization. Else, just use gradient.
USE_SECOND_ORDER = False
# HUMAN_BETA = float('inf'): human is rational (and thus deterministic), 
# HUMAN_BETA is None: strategic value is not used
# else: human is noisily rational
HUMAN_BETA = None #0.01
MIN_STRAT_VAL = 0.0 # minimum strategic value (set dynamically)
# maximum strategic value (calculated based on theoretical reward)
MAX_STRAT_VAL = STRATEGIC_VALUE_SCALE * 1144.0
# if True, project tactical states outside of the strategic grid back onto the grid
PROJECT_ONTO_STRAT_GRID = False

### Reward
# reward weights
W_LANES = 1.25 # stay in center of lane
W_FENCES = -50.0 # stay on the road (i.e. away from fences on sides of road)
W_SPEED = -10.0 # keep at goal speed
W_OTHER_CAR_TRAJS = -80.0 # stay away from other cars
W_OTHER_TRUCK_TRAJS = -40.0 # stay away from other trucks
W_BEHIND = -3.0 # don't be behind the other car
W_CONTROL = -0.1 # cost for control
W_BOUNDED_CONTROL = -100.0 # don't violate control bounds
# reward settings
FINE_BEHIND_R = False # if True, robot car is not penalized for being behind the human car
FINE_BEHIND_H = True # if True, human car is not penalized for being behind the robot car
FENCE_SIGMOID = True # if True, fence reward is a sigmoid. Otherwise, gaussian

### Plotting
# Size/courseness of heatmap: (y size, x size). Must be square. Larger size 
# results in a finer (more detailed) heatmap. 
# Original (large) size: (256, 256)
# Medium size: (128, 128)
# Smaller size (faster to compute): (32, 32)
HEATMAP_SIZE = (32, 32)
# if True, show heatmap for the whole visible screen. Otherwise, just for 
# (approximately) the road and a small area to the side of the road.
FULL_HEATMAP = False

