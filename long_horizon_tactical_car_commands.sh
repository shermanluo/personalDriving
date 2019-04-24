### in-depth case study commands

## vs. SimpleOptimizerCar
# overtaking
# python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
# # easy_merging
# python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
# # hard_merging
# python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_simple_optimizer_car
# # far_overtaking
# python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human SimpleOptimizerCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_simple_optimizer_car

## vs. FollowerCar
# overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_follower_car
    # python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_follower_car
# easy_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_follower_car
    # python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_follower_car
# hard_merging
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_follower_car
    # python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_follower_car
# far_overtaking
python run.py world_tactical_long_horizon_overtaking -n -t 150 -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human FollowerCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_follower_car
    # python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_follower_car

## vs. UserControlledCar
# overtaking
# python run.py world_tactical_long_horizon_overtaking -b 1 -x 'overtaking' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/overtaking_long_tactical_inf_timeup_vs_user_controlled_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'overtaking' -l deep_case_study/overtaking_long_tactical_inf_timeup_vs_user_controlled_car
# # easy_merging
# python run.py world_tactical_long_horizon_overtaking -b 1 -x 'easy_merging' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/easy_merging_long_tactical_inf_timeup_vs_user_controlled_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'easy_merging' -l deep_case_study/easy_merging_long_tactical_inf_timeup_vs_user_controlled_car
# # hard_merging
# python run.py world_tactical_long_horizon_overtaking -b 1 -x 'hard_merging' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/hard_merging_long_tactical_inf_timeup_vs_user_controlled_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'hard_merging' -l deep_case_study/hard_merging_long_tactical_inf_timeup_vs_user_controlled_car
# # far_overtaking
# python run.py world_tactical_long_horizon_overtaking -b 1 -x 'far_overtaking' -o inf -d 4 -r 0 --human UserControlledCar -s deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_user_controlled_car
#     python run.py world_tactical_long_horizon_overtaking -f -x 'far_overtaking' -l deep_case_study/far_overtaking_long_tactical_inf_timeup_vs_user_controlled_car
