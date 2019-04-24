#!/bin/bash
set -eux

### commands to run tactical short horizon car with Hessian and different plan initializations vs. SimpleOptimizerCar

# overtaking
python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/overtaking_short_tactical_vs_simple_optimizer_car -n
python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/overtaking_short_tactical_vs_simple_optimizer_car -f --plan

# far_overtaking
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/far_overtaking_short_tactical_vs_simple_optimizer_car -n
python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/far_overtaking_short_tactical_vs_simple_optimizer_car -f --plan

# easy_merging
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/easy_merging_short_tactical_vs_simple_optimizer_car -n
python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/easy_merging_short_tactical_vs_simple_optimizer_car -f --plan

# hard_merging
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/hard_merging_short_tactical_vs_simple_optimizer_car -n
python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/hard_merging_short_tactical_vs_simple_optimizer_car -f --plan


### commands to run tactical long horizon car with Hessian and different plan initializations vs. SimpleOptimizerCar

# overtaking
python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/overtaking_long_tactical_vs_simple_optimizer_car -n

# far_overtaking
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/far_overtaking_long_tactical_vs_simple_optimizer_car -n

# easy_merging
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/easy_merging_long_tactical_vs_simple_optimizer_car -n

# hard_merging
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/hard_merging_long_tactical_vs_simple_optimizer_car -n


### commands to run tactical short horizon car with Hessian and different plan initializations vs. FollowerCar

# overtaking
python run.py world_highway -x overtaking -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/overtaking_short_tactical_vs_follower_car -n

# far_overtaking
python run.py world_highway -x far_overtaking -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/far_overtaking_short_tactical_vs_follower_car -n

# easy_merging
python run.py world_highway -x easy_merging -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/easy_merging_short_tactical_vs_follower_car -n

# hard_merging
python run.py world_highway -x hard_merging -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 -u -s tactical_hessian_plan_init_case_studies/hard_merging_short_tactical_vs_follower_car -n


### commands to run tactical long horizon car with Hessian and different plan initializations vs. FollowerCar

# overtaking
python run.py world_highway -x overtaking -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/overtaking_long_tactical_vs_follower_car -n

# far_overtaking
python run.py world_highway -x far_overtaking -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/far_overtaking_long_tactical_vs_follower_car -n

# easy_merging
python run.py world_highway -x easy_merging -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/easy_merging_long_tactical_vs_follower_car -n

# hard_merging
python run.py world_highway -x hard_merging -t 150 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u -s tactical_hessian_plan_init_case_studies/hard_merging_long_tactical_vs_follower_car -n





### commands to visual interaction of tactical short horizon car with Hessian and different plan initializations

## vs. SimpleOptimizerCar

# overtaking
python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/overtaking_short_tactical_vs_simple_optimizer_car -f

# far_overtaking
python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/far_overtaking_short_tactical_vs_simple_optimizer_car -f

# easy_merging
python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/easy_merging_short_tactical_vs_simple_optimizer_car -f

# hard_merging
python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/hard_merging_short_tactical_vs_simple_optimizer_car -f

## vs. FollowerCar

# overtaking
python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/overtaking_short_tactical_vs_follower_car -f

# far_overtaking
python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/far_overtaking_short_tactical_vs_follower_car -f

# easy_merging
python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/easy_merging_short_tactical_vs_follower_car -f

# hard_merging
python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/hard_merging_short_tactical_vs_follower_car -f



### commands to visual interaction of tactical long horizon car with Hessian and different plan initializations

## vs. SimpleOptimizerCar

# overtaking
python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/overtaking_long_tactical_vs_simple_optimizer_car -f

# far_overtaking
python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/far_overtaking_long_tactical_vs_simple_optimizer_car -f

# easy_merging
python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/easy_merging_long_tactical_vs_simple_optimizer_car -f

# hard_merging
python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/hard_merging_long_tactical_vs_simple_optimizer_car -f

## vs. FollowerCar

# overtaking
python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/overtaking_long_tactical_vs_follower_car -f

# far_overtaking
python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/far_overtaking_long_tactical_vs_follower_car -f

# easy_merging
python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/easy_merging_long_tactical_vs_follower_car -f

# hard_merging
python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/hard_merging_long_tactical_vs_follower_car -f
