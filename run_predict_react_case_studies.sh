### predict then react studies
## vs. SimpleOptimizerCar
# overtaking
python run.py world_highway -n -t 150 -x 'overtaking' -o inf --robot PredictReactCar --human SimpleOptimizerCar -s predict_react_case_studies/overtaking_predict_react_inf_timeup_vs_simple_optimizer_car
python run.py world_highway -f --heatmap r_tact -x 'overtaking' --robot PredictReactCar --human SimpleOptimizerCar -l predict_react_case_studies/overtaking_predict_react_inf_timeup_vs_simple_optimizer_car

# easy_merging
# python run.py world_highway -n -t 150  -x 'easy_merging' -o inf --robot PredictReactCar --human SimpleOptimizerCar -s predict_react_case_studies/easy_merging_predict_react_inf_timeup_vs_simple_optimizer_car
python run.py world_highway -f --heatmap r_tact -x 'easy_merging' --robot PredictReactCar --human SimpleOptimizerCar -l predict_react_case_studies/easy_merging_predict_react_inf_timeup_vs_simple_optimizer_car

# hard_merging
# python run.py world_highway -n -t 150  -x 'hard_merging' -o inf --robot PredictReactCar --human SimpleOptimizerCar -s predict_react_case_studies/hard_merging_predict_react_inf_timeup_vs_simple_optimizer_car
python run.py world_highway -f --heatmap r_tact -x 'hard_merging' --robot PredictReactCar --human SimpleOptimizerCar -l predict_react_case_studies/hard_merging_predict_react_inf_timeup_vs_simple_optimizer_car

# far overtaking
# python run.py world_highway -n -t 150  -x 'far_overtaking' -o inf --robot PredictReactCar --human SimpleOptimizerCar -s predict_react_case_studies/far_overtaking_predict_react_inf_timeup_vs_simple_optimizer_car
python run.py world_highway -f --heatmap r_tact -x 'far_overtaking' --robot PredictReactCar --human SimpleOptimizerCar -l predict_react_case_studies/far_overtaking_predict_react_inf_timeup_vs_simple_optimizer_car
