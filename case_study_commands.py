"""
* 3 different scenarios: 
    1) overtaking where the robot starts behind the human in the same lane, 
    2) "hard" merging where the robot starts next to or a bit behind the human in the adjacent lane, 
    3) "easy" merging where the robot starts in front of the human in the adjacent lane with enough room to merge easily.
    4) "far" overtaking where the robot starts farther behind the human in the same lane, 

* 3 different algorithms: 
    1) tactical car without strategic value, 
    2) hierarchical car with 3D strategic value, 
    3) hierarchical car with 4D strategic value.

* 2 different optimization timeouts: 
    inf
    0.1 - don't do this yet
"""

### main case studies

## vs. SimpleOptimizerCar
# overtaking
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s main_case_studies/overtaking_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 3 -r 5 --human SimpleOptimizerCar -s main_case_studies/overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'overtaking' -o inf -d 4 -r 5 --human SimpleOptimizerCar -s main_case_studies/overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# easy_merging
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s main_case_studies/easy_merging_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 3 -r 5 --human SimpleOptimizerCar -s main_case_studies/easy_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'easy_merging' -o inf -d 4 -r 5 --human SimpleOptimizerCar -s main_case_studies/easy_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# hard_merging
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s main_case_studies/hard_merging_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 3 -r 5 --human SimpleOptimizerCar -s main_case_studies/hard_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'hard_merging' -o inf -d 4 -r 5 --human SimpleOptimizerCar -s main_case_studies/hard_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# far overtaking
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 3 -r 5 --human SimpleOptimizerCar -s main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'far_overtaking' -o inf -d 4 -r 5 --human SimpleOptimizerCar -s main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

## vs. FollowerCar
# overtaking
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human FollowerCar -s main_case_studies/overtaking_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 3 -r 5 --human FollowerCar -s main_case_studies/overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'overtaking' -o inf -d 4 -r 5 --human FollowerCar -s main_case_studies/overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'overtaking' -l main_case_studies/overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# easy_merging
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human FollowerCar -s main_case_studies/easy_merging_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 3 -r 5 --human FollowerCar -s main_case_studies/easy_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'easy_merging' -o inf -d 4 -r 5 --human FollowerCar -s main_case_studies/easy_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'easy_merging' -l main_case_studies/easy_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# hard_merging
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human FollowerCar -s main_case_studies/hard_merging_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 3 -r 5 --human FollowerCar -s main_case_studies/hard_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'hard_merging' -o inf -d 4 -r 5 --human FollowerCar -s main_case_studies/hard_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'hard_merging' -l main_case_studies/hard_merging_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# far overtaking
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human FollowerCar -s main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 3 -r 5 --human FollowerCar -s main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'far_overtaking' -o inf -d 4 -r 5 --human FollowerCar -s main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

# far overtaking
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human FollowerCar -s main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_tactical_inf_timeup_vs_simple_optimizer_car
python run.py world_hierarchical_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 3 -r 5 --human FollowerCar -s main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_3d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat
python run.py world_hierarchical_overtaking -n -t 300 -b 1 -x 'far_overtaking' -o inf -d 4 -r 5 --human FollowerCar -s main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_simple_optimizer_car --heatmap r_strat

## vs. UserControlledCar
# far overtaking
python run.py world_hierarchical_overtaking -b 1 -x 'far_overtaking' -o inf -d 4 -r 5 --human UserControlledCar -s main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_user_controlled_car
    python run.py world_hierarchical_overtaking -f -x 'far_overtaking' -l main_case_studies/far_overtaking_4d_strat_val_inf_timeup_vs_user_controlled_car

### in-depth case study

## vs. SimpleOptimizerCar
# overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
# easy_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
# hard_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
# far_overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car

## vs. FollowerCar
# overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_follower_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_follower_car
# easy_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_follower_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_follower_car
# hard_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_follower_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_follower_car
# far_overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_follower_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_follower_car

## vs. UserControlledCar
# overtaking
python run.py world_tactical_long_horizon_overtaking -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_user_controlled_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_user_controlled_car
# easy_merging
python run.py world_tactical_long_horizon_overtaking -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_user_controlled_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_user_controlled_car
# hard_merging
python run.py world_tactical_long_horizon_overtaking -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_user_controlled_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_user_controlled_car
# far_overtaking
python run.py world_tactical_long_horizon_overtaking -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_user_controlled_car
    python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_user_controlled_car
