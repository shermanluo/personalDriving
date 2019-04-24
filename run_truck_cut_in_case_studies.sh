set -eux

### truck cut-in case studies

################################################################################
## vs. SimpleOptimizerCar
################################################################################

# Vary how far away the human and robot are from the truck.
# ROOT_DIR="truck_cut_in_case_studies/"

# f = 2 ==> not enough space to overtake
# f = 2.1 ==> barely enough space to overtake
# f = 2.2 ==> enough space to overtake
# for f in 1.5 2 2.1 2.2 2.3 2.5; do
# for f in 2.125 2.15 2.175; do
#     # python run.py world_highway_truck_cut_in -n -t 300 -x 'truck_cut_in_human_in_front' -fyr $f --robot HierarchicalCar --human SimpleOptimizerCar -b 1 -d 5 -o inf -s "$ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_simple_optimizer_car"
#     python run.py world_highway_truck_cut_in -f --heatmap r_strat -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human SimpleOptimizerCar -l "$ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_simple_optimizer_car"
# done

# v = 1.01501502 ==> robot doesn't have enough space to overtake. Gets caught behind truck and slows down without switching back to left lane
# v = 1.09309309 ==> robot doesn't have enough space to overtake. Gets caught behind truck and slows down without switching back to left lane
# v = 1.17117117 ==> robot has enough space to overtake (this is the default velocity)
# for v in 0.7027027 0.78078078 0.85885886 0.93693694 1.01501502 1.09309309 1.17117117 1.24924925 1.32732733 1.40540541; do
# for v in 1.1126 1.1321 1.1517; do
#     # python run.py world_highway_truck_cut_in -n -t 300 -x 'truck_cut_in_human_in_front' -vr0 $v --robot HierarchicalCar --human SimpleOptimizerCar -b 1 -d 5 -o inf -s "$ROOT_DIR""vary_vr0/truck_cut_in_""$v""_hierarchical_vs_simple_optimizer_car"
#     python run.py world_highway_truck_cut_in -f --heatmap r_strat -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human SimpleOptimizerCar -l "$ROOT_DIR""vary_vr0/truck_cut_in_""$v""_hierarchical_vs_simple_optimizer_car"
# done


################################################################################
### longer y_rel grid
################################################################################
## vs. FollowerCar

# LONGER_YREL_ROOT_DIR="truck_cut_in_longer_yrel_case_studies/"


# for f in 4.8; do
#     # python run.py world_highway_truck_cut_in -n -t 200 -x 'truck_cut_in_human_in_front' -fyr $f --robot HierarchicalCar --human FollowerCar -b 1 -d 5 -o inf -s "$LONGER_YREL_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_follower_car"
#     python run.py world_highway_truck_cut_in -f --plan --heatmap r_strat -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$LONGER_YREL_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_follower_car"
# done

# for v in 1.3 1.5 1.7; do
#     # python run.py world_highway_truck_cut_in -n -t 200 -x 'truck_cut_in_human_in_front' -vr0 $v --robot HierarchicalCar --human FollowerCar -b 1 -d 5 -o inf -s "$LONGER_YREL_ROOT_DIR""vary_vr0/truck_cut_in_""$v""_hierarchical_vs_follower_car"
#     python run.py world_highway_truck_cut_in -f --plan -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$LONGER_YREL_ROOT_DIR""vary_vr0/truck_cut_in_""$v""_hierarchical_vs_follower_car"
# done

# python run.py world_highway_truck_cut_in -f --heatmap r_strat -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l truck_cut_in_longer_yrel_case_studies/vary_yrel_from_truck/truck_cut_in_4.9_hierarchical_vs_follower_car

################################################################################
## vs. FollowerCar, projecting onto strategic grid
################################################################################

STRAT_PROJECT_ROOT_DIR="truck_cut_in_project_strategic_grid_case_studies/"

for f in 4; do
    # python run.py world_highway_truck_cut_in -n -t 200 -x 'truck_cut_in_human_in_front' -fyr $f --robot HierarchicalCar --human FollowerCar -b 1 -d 5 -o inf --proj_strat_grid -s "$STRAT_PROJECT_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_follower_car"
    python run.py world_highway_truck_cut_in -f --plan --heatmap r_strat --proj_strat_grid -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_""$f""_hierarchical_vs_follower_car"
done


################################################################################
### human lets robot in
################################################################################
# HUMAN_LETS_ROBOT_IN_ROOT_DIR="truck_cut_in_hard_merge_human_lets_robot_in_case_studies/"


# for f in 2; do
#     # python run.py world_highway_truck_cut_in -n -t 100 -x 'truck_cut_in_hard_merge_human_lets_robot_in' -fyr $f --robot HierarchicalCar --human FollowerCar -b 1 -d 5 -o inf -s "$HUMAN_LETS_ROBOT_IN_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_lets_robot_in_""$f""_hierarchical_vs_follower_car"
#     # python run.py world_highway_truck_cut_in -f --plan --heatmap r_strat -x 'truck_cut_in_hard_merge_human_lets_robot_in' --robot HierarchicalCar --human FollowerCar -l "$HUMAN_LETS_ROBOT_IN_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_lets_robot_in_""$f""_hierarchical_vs_follower_car"
#     python run.py world_highway_truck_cut_in -f --plan --heatmap h_strat -x 'truck_cut_in_hard_merge_human_lets_robot_in' --robot HierarchicalCar --human FollowerCar -l "$HUMAN_LETS_ROBOT_IN_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_lets_robot_in_""$f""_hierarchical_vs_follower_car"
# done

################################################################################
# ### human cuts robot off
################################################################################
# HUMAN_CUTS_OFF_ROBOT_ROOT_DIR="truck_cut_in_hard_merge_human_cuts_off_robot_case_studies/"

# for f in 2; do
#     # python run.py world_highway_truck_cut_in -n -t 100 -x 'truck_cut_in_hard_merge_human_cuts_off_robot' -fyr $f --robot HierarchicalCar --human FollowerCar -b 1 -d 5 -o inf -s "$HUMAN_CUTS_OFF_ROBOT_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_cuts_off_robot_""$f""_hierarchical_vs_follower_car"
#     python run.py world_highway_truck_cut_in -f --plan --heatmap r_strat -x 'truck_cut_in_hard_merge_human_cuts_off_robot' --robot HierarchicalCar --human FollowerCar -l "$HUMAN_CUTS_OFF_ROBOT_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_cuts_off_robot_""$f""_hierarchical_vs_follower_car"
#     python run.py world_highway_truck_cut_in -f --plan --heatmap h_strat -x 'truck_cut_in_hard_merge_human_cuts_off_robot' --robot HierarchicalCar --human FollowerCar -l "$HUMAN_CUTS_OFF_ROBOT_ROOT_DIR""vary_yrel_from_truck/truck_cut_in_hard_merge_human_cuts_off_robot_""$f""_hierarchical_vs_follower_car"
# done


################################################################################
# manual
################################################################################
python run.py world_highway_truck_cut_in -m --proj_strat_grid -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -b 1 -d 5

