set -eux

STRAT_DIM=4

### predict then react car with/without strategic value for the car overtaking scenario

ROOT_DIR="predict_react_with_and_without_strategic_value_case_studies/"

################################################################################
### overtaking
################################################################################

### with strategic value vs. simple optimizer car
WITH_STRAT_VAL_ROOT_DIR="$ROOT_DIR""with_strategic_value_human_ignores_robot_no_proj_strat_grid/"

# python run.py world_highway -n -t 300 -x 'far_overtaking' --h_ignore_r --robot PredictReactHierarchicalCar --human SimpleOptimizerCar -b 1 -d $STRAT_DIM -o inf -s "$WITH_STRAT_VAL_ROOT_DIR""far_overtaking_vs_simple_optimizer_car"
python run.py world_highway -f -x 'far_overtaking' --plan --heatmap r_strat --robot PredictReactHierarchicalCar --human SimpleOptimizerCar -b 1 -d $STRAT_DIM -l "$WITH_STRAT_VAL_ROOT_DIR""far_overtaking_vs_simple_optimizer_car"

### with strategic value vs. follower car

# python run.py world_highway -n -t 300 -x 'far_overtaking' --h_ignore_r --robot PredictReactHierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM -o inf -s "$WITH_STRAT_VAL_ROOT_DIR""far_overtaking_vs_follower_car"
python run.py world_highway -f -x 'far_overtaking' --plan --heatmap r_strat --robot PredictReactHierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM -l "$WITH_STRAT_VAL_ROOT_DIR""far_overtaking_vs_follower_car"

### without strategic value vs. simple optimizer car
# WITHOUT_STRAT_VAL_ROOT_DIR="$ROOT_DIR""without_strategic_value_human_ignores_robot/"

# python run.py world_highway -n -t 200 -x 'far_overtaking' --h_ignore_r --robot PredictReactCar --human SimpleOptimizerCar -o inf -s "$WITHOUT_STRAT_VAL_ROOT_DIR""far_overtaking_vs_simple_optimizer_car"
# python run.py world_highway -f -x 'far_overtaking' --plan --robot PredictReactCar --human SimpleOptimizerCar -l "$WITHOUT_STRAT_VAL_ROOT_DIR""far_overtaking_vs_simple_optimizer_car"

### without strategic value vs. follower car
# python run.py world_highway -n -t 200 -x 'far_overtaking' --h_ignore_r --robot PredictReactCar --human FollowerCar -o inf -s "$WITHOUT_STRAT_VAL_ROOT_DIR""far_overtaking_vs_follower_car"
# python run.py world_highway -f -x 'far_overtaking' --plan --robot PredictReactCar --human FollowerCar -l "$WITHOUT_STRAT_VAL_ROOT_DIR""far_overtaking_vs_follower_car"


################################################################################
# manual
################################################################################
# python run.py world_highway_truck_cut_in -m -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM --proj_strat_grid --heat_val_show


