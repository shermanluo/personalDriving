#!/bin/bash
set -eux

##### Tactical car

#### long horizon

### previous optimal plan init scheme

## with Hessian
# WILL TAKE TOO LONG ON THIS COMPUTER
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l long_tactical_hessian_plan_init_case_studies/long_prev_opt_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l long_tactical_hessian_plan_init_case_studies/long_prev_opt_hessian_overtaking_vs_simple_optimizer_car -f --plan
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l long_tactical_hessian_plan_init_case_studies/long_prev_opt_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l long_tactical_hessian_plan_init_case_studies/long_prev_opt_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## without Hessian
# ALREADY DONE
# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_prev_opt_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_prev_opt_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_prev_opt_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_prev_opt_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan

### maintain speed lsr (left straight right) plan init scheme

## without Hessian
# far overtaking vs. SimpleOptimizerCar
python run.py world_highway -x far_overtaking -l all_case_studies/long_maintain_speed_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_maintain_speed_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
python run.py world_highway -x easy_merging -l all_case_studies/long_maintain_speed_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -l all_case_studies/long_maintain_speed_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## with Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_maintain_speed_lsr_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_maintain_speed_lsr_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_maintain_speed_lsr_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_maintain_speed_lsr_hessian_hard_merging_vs_simple_optimizer_car -f --plan

### maintain_speed_prev_steer plan init scheme

## without Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_maintain_speed_prev_steer_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_maintain_speed_prev_steer_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_maintain_speed_prev_steer_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_maintain_speed_prev_steer_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## with Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_maintain_speed_prev_steer_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_maintain_speed_prev_steer_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_maintain_speed_prev_steer_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_maintain_speed_prev_steer_hessian_hard_merging_vs_simple_optimizer_car -f --plan

### max_speed_prev_steer plan init scheme

## without Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_max_speed_prev_steer_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_max_speed_prev_steer_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_max_speed_prev_steer_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_max_speed_prev_steer_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## with Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_max_speed_prev_steer_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_max_speed_prev_steer_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/long_max_speed_prev_steer_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/long_max_speed_prev_steer_hessian_hard_merging_vs_simple_optimizer_car -f --plan

### lsr (left straight right) init scheme

## with Hessian
# WILL TAKE TOO LONG ON THIS COMPUTER
# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_hessian_far_overtaking_vs_simple_optimizer_car -n
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_hessian_overtaking_vs_simple_optimizer_car -n
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_hessian_easy_merging_vs_simple_optimizer_car -n
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 -u --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_hessian_hard_merging_vs_simple_optimizer_car -n

## without Hessian
# THESE DIDN'T ALL RUN SUCCESSFULLY YET
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/long_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/long_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -n
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 20 -r 0 --init_plan_scheme_r lsr --init_plan_scheme_h prev_opt -s all_case_studies/long_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -n


#### short horizon

### previous optimal plan init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l tactical_hessian_plan_init_case_studies/short_prev_opt_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l tactical_hessian_plan_init_case_studies/short_prev_opt_hessian_overtaking_vs_simple_optimizer_car -f --plan
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l tactical_hessian_plan_init_case_studies/short_prev_opt_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l tactical_hessian_plan_init_case_studies/short_prev_opt_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## without Hessian
# ALREADY DONE                
# far overtaking vs. SimpleOptimizerCar
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/short_prev_opt_no_hessian_far_overtaking_vs_simple_optimizer_car -n
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/short_prev_opt_no_hessian_overtaking_vs_simple_optimizer_car -n
# easy merging vs. SimpleOptimizerCar
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/short_prev_opt_no_hessian_easy_merging_vs_simple_optimizer_car -n
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 5 -r 0 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/short_prev_opt_no_hessian_hard_merging_vs_simple_optimizer_car -n

### maintain speed lsr (left straight right) plan init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/short_maintain_speed_lsr_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/short_maintain_speed_lsr_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/short_maintain_speed_lsr_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/short_maintain_speed_lsr_hessian_hard_merging_vs_simple_optimizer_car -f --plan

## without Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/short_maintain_speed_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/short_maintain_speed_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/short_maintain_speed_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/short_maintain_speed_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan

### lsr (left straight right) init scheme

## with Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/short_lsr_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/short_lsr_hessian_overtaking_vs_simple_optimizer_car -f --plan
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/short_lsr_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/short_lsr_hessian_hard_merging_vs_simple_optimizer_car -f --plan

# ## without Hessian

# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/short_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --plan
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/short_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --plan
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/short_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -f --plan
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/short_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -f --plan



##### Hierarchical car

#### 3D short horizon

### previous optimal plan init scheme

## with Hessian
# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/3d_strat_val_prev_opt_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/3d_strat_val_prev_opt_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/3d_strat_val_prev_opt_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/3d_strat_val_prev_opt_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat

## without Hessian
# far overtaking vs. SimpleOptimizerCar
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/3d_strat_val_prev_opt_no_hessian_far_overtaking_vs_simple_optimizer_car -n
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/3d_strat_val_prev_opt_no_hessian_overtaking_vs_simple_optimizer_car -n
# easy merging vs. SimpleOptimizerCar
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/3d_strat_val_prev_opt_no_hessian_easy_merging_vs_simple_optimizer_car -n
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/3d_strat_val_prev_opt_no_hessian_hard_merging_vs_simple_optimizer_car -n


### lsr (left straight right) init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/3d_strat_val_lsr_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
python run.py world_highway -x overtaking -l all_case_studies/3d_strat_val_lsr_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/3d_strat_val_lsr_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -l all_case_studies/3d_strat_val_lsr_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan

## without Hessian

# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/3d_strat_val_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/3d_strat_val_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/3d_strat_val_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/3d_strat_val_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan

# #### 4D short horizon

### previous optimal plan init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_prev_opt_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_prev_opt_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_prev_opt_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_prev_opt_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat

## without Hessian
# (overtaking strategy)
# far overtaking vs. SimpleOptimizerCar
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_far_overtaking_vs_simple_optimizer_car -n
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_overtaking_vs_simple_optimizer_car -n
# easy merging vs. SimpleOptimizerCar
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_easy_merging_vs_simple_optimizer_car -n
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_hard_merging_vs_simple_optimizer_car -n

# (tailgating strategy)
# far overtaking vs. UserControlledCar
python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_far_overtaking_vs_user_controlled_car -n
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_overtaking_vs_user_controlled_car -n
# easy merging vs. SimpleOptimizerCar
python run.py world_highway -x easy_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_easy_merging_vs_user_controlled_car -n
# hard merging vs. SimpleOptimizerCar
python run.py world_highway -x hard_merging -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r prev_opt --init_plan_scheme_h prev_opt -s all_case_studies/4d_strat_val_prev_opt_no_hessian_hard_merging_vs_user_controlled_car -n


### maintain_speed_prev_steer plan init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan

## without Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_no_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_no_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_no_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_maintain_speed_prev_steer_no_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan

### max_speed_prev_steer plan init scheme

## with Hessian

# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_max_speed_prev_steer_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_max_speed_prev_steer_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_max_speed_prev_steer_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_max_speed_prev_steer_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan

## without Hessian
# far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_max_speed_prev_steer_no_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_max_speed_prev_steer_no_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat --plan
# easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_max_speed_prev_steer_no_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan
# hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_max_speed_prev_steer_no_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat --plan


# ### lsr (left straight right) init scheme

## with Hessian

# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_lsr_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_lsr_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_lsr_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_lsr_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat

## without Hessian

# # far overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x far_overtaking -l all_case_studies/4d_strat_val_lsr_no_hessian_far_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # overtaking vs. SimpleOptimizerCar
# python run.py world_highway -x overtaking -l all_case_studies/4d_strat_val_lsr_no_hessian_overtaking_vs_simple_optimizer_car -f --heatmap r_strat
# # easy merging vs. SimpleOptimizerCar
# python run.py world_highway -x easy_merging -l all_case_studies/4d_strat_val_lsr_no_hessian_easy_merging_vs_simple_optimizer_car -f --heatmap r_strat
# # hard merging vs. SimpleOptimizerCar
# python run.py world_highway -x hard_merging -l all_case_studies/4d_strat_val_lsr_no_hessian_hard_merging_vs_simple_optimizer_car -f --heatmap r_strat
