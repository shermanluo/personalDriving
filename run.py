import argparse
import pdb
import pickle
import sys
import theano as th

from car import UserControlledCar
import config
import constants
import visualize
import world


th.config.optimizer_verbose = False
th.config.allow_gc = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # Settings of this interaction
    parser.add_argument('world', 
        help="The name of the world to run.")
    parser.add_argument('-x', '--init_state', 
        default=constants.INITIAL_STATE_OPTIONS[0], 
        choices=constants.INITIAL_STATE_OPTIONS,
        help="Which initial state configuration to start in.")
    parser.add_argument('-fyr', '--front_y_rel', type=float, default=config.FRONT_Y_REL,
        help="Initial relative y-distance between the truck and the car in front (y_truck - y_front_car). Only applicable for the truck cut-in scenarios.")
    parser.add_argument('-vr0', '--init_speed_r', type=float, default=config.INITIAL_SPEED_R,
        help="Initial speed of the robot.")
    parser.add_argument('-t', '--iters', default=None,
        help="Maximum number of iterations to run the visualization.")
    parser.add_argument('--human', default=constants.HUMAN_CAR_OPTIONS[0], 
        choices=constants.HUMAN_CAR_OPTIONS,
        help="The type of the human car.")
    parser.add_argument('--robot', default=constants.ROBOT_CAR_OPTIONS[0], 
        choices=constants.ROBOT_CAR_OPTIONS,
        help="The type of the robot car.")

    # Visualization
    parser.add_argument('--heatmap', default=None, choices=constants.HEATMAP_OPTIONS,
        help="Visualize the specified heatmap.")
    parser.add_argument('--plan', action='store_true',
        help="Visualize the plans.")
    parser.add_argument('--heat_val_show', action='store_true',
        help="Display the value of the heat at the current mouse location.")
    
    # Planning algorithm settings
    parser.add_argument('-b', '--beta', default=None,
        help="Human beta value.")
    parser.add_argument('-d', '--strat_dim', default=4,
        help="Dimension of the strategic value.")
    parser.add_argument('-psg', '--proj_strat_grid', action='store_true',
        help="If True, project tactical states outside of the strategic grid back onto the grid.")
    parser.add_argument('-o', '--opt_timeout', default=0.1,
        help="Maximum time for optimization of the plan.")
    parser.add_argument('--horizon', type=int, default=config.HORIZON,
        help="Maximum time for optimization of the plan.")
    parser.add_argument('-r', '--strat_val_scale', default=5,
        help="Scaling of the strategic value.")
    parser.add_argument('-u', '--use_second_order', action='store_true',
        help="If True, use second order terms in the nested optimization.")
    parser.add_argument('--init_plan_scheme_r', 
        default=constants.INIT_PLAN_SCHEMES_OPTIONS[0],
        choices=constants.INIT_PLAN_SCHEMES_OPTIONS,
        help="Plan initialization scheme for the robot car.")
    parser.add_argument('--init_plan_scheme_h', 
        default=constants.INIT_PLAN_SCHEMES_OPTIONS[0],
        choices=constants.INIT_PLAN_SCHEMES_OPTIONS,
        help="Plan initialization scheme for the human car.")
    parser.add_argument('--h_ignore_r', action='store_true',
        help="If True, robot will predict that human's reward is independent of the robot's \
              # trajectory (i.e. human ignores the robot).")

    # Saving data from this interaction
    parser.add_argument('-s', '--save_interaction_data_dir', default=None,
        help="Filename inside of the global interaction data directory to which to save the interaction data.")
    parser.add_argument('-f', '--save_frames', action='store_true',
        help="Directory inside of the global interaction frame directory in which to save the frames of the interaction.")
    
    # Loading data for this interaction
    parser.add_argument('-l', '--load_interaction_data_dir', default=None,
        help="Directory inside of the interaction data directory containing the interaction data to visualize.")
    
    # Other modes
    parser.add_argument('-m', '--manual', action='store_true',
        help="Manual mode, which does not have optimization and allows the user to manually set the cars' states.")
    parser.add_argument('-n', '--no_vis', action='store_true',
        help="Run the interaction without visualization.")
    # parser.add_argument('--save_then_load', action='store_true',
    #     help="First run the interaction without visualization and save the interaction data, then load it and do the desired visualization.")
    
    # Theano configuration
    parser.add_argument('--fast', action='store_true',
        help="If True, set Theano config.optimizer to 'fast_compile'.")
    parser.add_argument('--FAST', action='store_true',
        help="If True, set Theano config.mode to 'FAST_COMPILE'.")
    args = parser.parse_args(sys.argv[1:])

    ### configure Theano
    if args.fast:
        th.config.optimizer = 'fast_compile'
    if args.FAST:
        th.config.mode = 'FAST_COMPILE'

    ### World and algorithm setup
    
    # algorithm setup
    config.HUMAN_CAR = 'car.' + args.human
    config.ROBOT_CAR = 'car.' + args.robot
    # set robot's belief about the human's knowledge of the robot trajectory
    if args.robot == 'PredictReactCar':
        config.R_BELIEF_H_KNOWS_TRAJ_R = False
    else:
        config.R_BELIEF_H_KNOWS_TRAJ_R = True
    config.STRATEGIC_VALUE_SCALE = float(args.strat_val_scale)
    if int(args.strat_dim) != float(args.strat_dim):
        print 'Error: please provide an integer for the strategic dimension.'
    config.STRAT_DIM = int(args.strat_dim)
    config.OPT_TIMEOUT = float(args.opt_timeout) 
    config.HUMAN_BETA = args.beta
    config.USE_SECOND_ORDER = args.use_second_order
    config.HORIZON = args.horizon
    config.INIT_PLAN_SCHEME[constants.NAME_H] = args.init_plan_scheme_h
    config.INIT_PLAN_SCHEME[constants.NAME_R] = args.init_plan_scheme_r
    config.FRONT_Y_REL = args.front_y_rel
    config.INITIAL_SPEED_R = args.init_speed_r
    config.PROJECT_ONTO_STRAT_GRID = args.proj_strat_grid
    config.PREDICT_HUMAN_IGNORES_ROBOT = args.h_ignore_r
    
    init_planner = not (args.load_interaction_data_dir or args.manual)
    
    # load interaction data
    if args.load_interaction_data_dir is not None:
        if args.load_interaction_data_dir[-1] != '/':
            args.load_interaction_data_dir += '/'
        # config file for the interaction data
        config_interaction_data_filename = (constants.INTERACTION_DATA_DIR + 
            args.load_interaction_data_dir + 'config.pickle')
        with open(config_interaction_data_filename) as config_file:
            configuration = pickle.load(config_file)
        # set the config variables to those stored in the configuration file
        for var, value in configuration['config'].items():
            if type(value) == str:
                value = '"{0}"'.format(str(value)) # surround string with quotes
            elif value == float('inf'):
                value = "float('inf')" # replace inf with float('inf') to execute properly
            exec('config.{0} = {1}'.format(var, value))

        # interaction data file
        load_interaction_data_filename = (constants.INTERACTION_DATA_DIR + 
            args.load_interaction_data_dir + 'interaction_data.pickle')
        with open(load_interaction_data_filename) as data_file:
            interaction_data = pickle.load(data_file)
        this_world = getattr(world, args.world)(
            initial_states=args.init_state,
            interaction_data=interaction_data,
            init_planner=init_planner)
    else:
        this_world = getattr(world, args.world)(initial_states=args.init_state, 
            init_planner=init_planner)

    ### Visualizer setup
    
    # Set max number of iterations for situations when it's necessary
    iters = args.iters
    if iters is not None:
        iters = int(args.iters)
    elif args.no_vis or args.save_interaction_data_dir is not None:
        iters = 1000
    
    # save interaction data
    if args.save_interaction_data_dir is not None:
        if args.save_interaction_data_dir[-1] != '/':
            args.save_interaction_data_dir += '/'
        save_interaction_data_dir = constants.INTERACTION_DATA_DIR + args.save_interaction_data_dir
    else:
        save_interaction_data_dir = None
    
    # frame directory
    frame_dir = None
    if args.save_frames:
        frame_dir_suffix = 'frames'
        if args.plan:
            frame_dir_suffix += '_plan'
        if args.heatmap is not None:
            frame_dir_suffix += '_heatmap_{0}'.format(args.heatmap)
        frame_dir_suffix += '/'
        if args.save_interaction_data_dir is not None:
            frame_dir = (constants.INTERACTION_DATA_DIR + 
                            args.save_interaction_data_dir + frame_dir_suffix)
        elif args.load_interaction_data_dir is not None:
            frame_dir = (constants.INTERACTION_DATA_DIR + 
                            args.load_interaction_data_dir + frame_dir_suffix)

    # create visualizer
    vis = visualize.Visualizer(this_world, 
            dt=constants.DT, 
            name=this_world.name,
            iters=iters,
            save_interaction_data=save_interaction_data_dir is not None,
            save_interaction_data_dir=save_interaction_data_dir,
            save_frames=args.save_frames,
            frame_dir=frame_dir,
            manual=args.manual,
            plan_show=args.plan,
            heatmap_show=args.heatmap is not None, 
            heatmap_name=args.heatmap,
            heat_val_show=args.heat_val_show)
    vis.main_car = this_world.main_human_car

    # Start the simulation
    if args.no_vis:
        print 'Starting simulation without visualization.'
        cont = True # if True, continue the control loop
        while cont:
            cont = vis.control_loop()
    else:
        print 'Starting visualization.'
        vis.run()
