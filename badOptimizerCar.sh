#!/bin/bash
set -eux

#EASY MERGING
#python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -l all_case_studies/3d_strat_val_prev_opt_no_hessian_easy_merging_vs_simple_optimizer_car
 python run.py world_highway -x easy_merging -t 150 --human FollowerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -l follower_studies/3d_strat_val_prev_opt_no_hessian_easy_merging_vs_follower_car