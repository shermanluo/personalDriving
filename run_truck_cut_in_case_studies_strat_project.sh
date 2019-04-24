set -eux

STRAT_DIM=6

### truck cut-in case studies with projection of states outside of the strategic grid back onto the grid

STRAT_PROJECT_ROOT_DIR="truck_cut_in_6d_project_strategic_grid_vabs_vs_follower_car_case_studies/"

################################################################################
### hard merge
################################################################################

### HierarchicalCar
STRAT_PROJECT_HARD_MERGE_ROOT_DIR="$STRAT_PROJECT_ROOT_DIR""hard_merge/"

for f in 1.2 1.5; do # 0.7 0.876 1.05 1.2 1.5 1.75
    for v in 1.15945946 1.22972973 1.3; do # 1.05 1.15945946 1.22972973 1.3 1.37027027
        # python run.py world_highway_truck_cut_in -n -t 100 -x 'truck_cut_in_hard_merge' -fyr $f -vr0 $v --proj_strat_grid --robot HierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM -o inf -s "$STRAT_PROJECT_HARD_MERGE_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
        # python run.py world_highway_truck_cut_in -f --heatmap r_strat --plan -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_HARD_MERGE_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
        # python run.py world_highway_truck_cut_in -f --heatmap h_strat --plan -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_HARD_MERGE_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
        python run.py world_highway_truck_cut_in -f --plan -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_HARD_MERGE_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
    done
done

### NestedCar
# STRAT_PROJECT_HARD_MERGE_NESTED_CAR_ROOT_DIR="$STRAT_PROJECT_ROOT_DIR""hard_merge_nested_car/"

# for f in 0.7 0.876 1.05; do
#     for v in 1.15945946 1.22972973 1.3 1.37027027; do
#         # python run.py world_highway_truck_cut_in -n -t 100 -x 'truck_cut_in_hard_merge' -fyr $f -vr0 $v --robot NestedCar --human FollowerCar -o inf -s "$STRAT_PROJECT_HARD_MERGE_NESTED_CAR_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
#         python run.py world_highway_truck_cut_in -f --plan -x 'truck_cut_in_hard_merge' --robot NestedCar --human FollowerCar -l "$STRAT_PROJECT_HARD_MERGE_NESTED_CAR_ROOT_DIR""truck_cut_in_hard_merge_""$f""_yrel_""$v""_vr0"
#     done
# done


################################################################################
### overtaking
################################################################################

### HierarchicalCar
# STRAT_PROJECT_OVERTAKING_ROOT_DIR="$STRAT_PROJECT_ROOT_DIR""overtaking/"

# for f in 2 3 4 5 6; do # 2 2.5 3 3.5 4 5 6; do
#     # python run.py world_highway_truck_cut_in -n -t 200 -x 'truck_cut_in_human_in_front' -fyr $f --proj_strat_grid --robot HierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM -o inf -s "$STRAT_PROJECT_OVERTAKING_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
#     python run.py world_highway_truck_cut_in -f --heatmap r_strat --plan -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_OVERTAKING_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
#     python run.py world_highway_truck_cut_in -f --heatmap h_strat --plan -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_OVERTAKING_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
#     # python run.py world_highway_truck_cut_in -f --plan -x 'truck_cut_in_human_in_front' --robot HierarchicalCar --human FollowerCar -l "$STRAT_PROJECT_OVERTAKING_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
# done

### NestedCar
# STRAT_PROJECT_OVERTAKING_NESTED_ROOT_DIR="$STRAT_PROJECT_ROOT_DIR""overtaking_nested_car/"

# for f in 4 5 6; do
#     # python run.py world_highway_truck_cut_in -n -t 200 -x 'truck_cut_in_human_in_front' -fyr $f --robot NestedCar --human FollowerCar -o inf -s "$STRAT_PROJECT_OVERTAKING_NESTED_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
#     python run.py world_highway_truck_cut_in -f --plan -x 'truck_cut_in_human_in_front' --robot NestedCar --human FollowerCar -l "$STRAT_PROJECT_OVERTAKING_NESTED_ROOT_DIR""truck_cut_in_overtaking_""$f""_yrel"
# done


################################################################################
# manual
################################################################################
# 0 50 1.57 35
# 0 38 1.57 24.7
# python run.py world_highway_truck_cut_in -m -x 'truck_cut_in_hard_merge' --robot HierarchicalCar --human FollowerCar -b 1 -d $STRAT_DIM --proj_strat_grid --heat_val_show


