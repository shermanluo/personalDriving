#### 4D short horizon
### maintain_speed_prev_steer plan init scheme
## without Hessian
# far overtaking vs. SimpleOptimizerCar

pre="beta_case_studies/4d_strat_val_beta_"
post="_maintain_speed_prev_steer_no_hessian_far_overtaking_vs_simple_optimizer_car"
for b in 1.00E-12 1.00E-10 1.00E-08 1.00E-05 1.00E-04 1.00E-03 3.00E-03 1.00E-02 3.00E-02 1.00E-01 3.00E-01 1.00E+00
do
    echo $b
    echo $pre$b$post
    # python run.py world_highway -x far_overtaking -t 150 --human SimpleOptimizerCar --robot HierarchicalCar -b $b -d 4 -o inf --horizon 5 -r 5 --init_plan_scheme_r maintain_speed_prev_steer --init_plan_scheme_h prev_opt -s $pre$b$post -n    
python run.py world_highway -x far_overtaking -l $pre$b$post -f --heatmap r_strat
    python run.py world_highway -x far_overtaking -l $pre$b$post -f --heatmap r_strat --plan
done

