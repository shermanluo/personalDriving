#!/usr/bin/env bash

#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --h_ignore_r --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test1 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test3 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test4 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test5 -n
#
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 8 -r 5 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test6 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 8 -r 5 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test7 -n
#
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 8 -r 5 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test8 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 8 -r 5 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test9 -n



#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test10 -n
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test11 -n
# 8 init for human
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test12 -n
# -8 init for human


##USING SIMPLEOPTIMIZERCAR FOR HUMAN
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --h_ignore_r --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test13 -n
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test14 -n
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test15 -n
#nestedIBR
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test17 -n
#nestedIBR run once
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test16 -n

#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test18 -n
#-8
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -s test19 -n
#8

#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --h_ignore_r --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test1
#assume human continues straight
#[10016.276605465424, 0.0, 10091.475858803246]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test3
#nested car
#[10037.861205594163, 0.0, 10094.564671674789]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test4
#nested car without the influence term
#[10017.918035932633, 0.0, 10094.601600116237]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test5
#initialized with nested, optimize r once
#[10040.147801975714, 0.0, 10095.01537110957]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test6
##hierarchical 4d using influence
##[9794.364215724278, 0.0, 10093.672390109401]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test7
##hierarchical 4d no influence
##[9918.960930328805, 0.0, 10019.911247838098]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test8
###hierarchical 3d using influence
##[9744.119832589184, 0.0, 10095.40630773838]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot HierarchicalCar -b 1 -d 3 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test9
##hierarchical 4d no influence
##[9747.729174220936, 0.0, 10095.495103241412]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test10
#initialized with nested, optimize all times
#[10037.475217463454, 0.0, 10095.23153006525]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test11
#[10037.463252232179, 0.0, 10095.237805334515]
#python run.py world_highway -x hard_merging -t 100 --human FollowerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test12
#[10037.469935435733, 0.0, 10095.239911020395]


#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --h_ignore_r --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test13
###[10026.849695192263, 0.0, 10095.507791459915]
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test14
###[10038.033426536345, 0.0, 10094.54372676017]
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot NestedCar -b 1 -d 4 -o inf --horizon 8 -r 0 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test15
###[10019.833602982499, 0.0, 10094.600647112875]
###nestedIBR
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test17
##[10037.728466273718, 0.0, 10095.21081006109]
###nestedIBR run once
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test16
###[10038.464007652698, 0.0, 10095.172073176802]
##-8
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test18
##[10037.819008675575, 0.0, 10095.210202923623]
##8
#python run.py world_highway -x hard_merging -t 100 --human SimpleOptimizerCar --robot IteratedBestResponseCar -b 1 -d 4 -o inf --horizon 8 -r 0 -u --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test19
##[10037.811824743621, 0.0, 10095.210314438797]

#python run.py world_highway_truck_cut_in -x truck_cut_in_hard_merge -t 100 --human FollowerCar --robot IteratedBestResponseCar -o inf --horizon 8 -r 0 -d 5 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test
#IBR -8
#[9647.974573965505, 0.0, 10090.93273291209]

#python run.py world_highway_truck_cut_in -x truck_cut_in_hard_merge -t 100 --human FollowerCar --robot IteratedBestResponseCar -o inf --horizon 8 -r 0 -d 5 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test3
#IBR 8
#[9646.53191478837, 0.0, 10090.928679369046]

#python run.py world_highway_truck_cut_in -x truck_cut_in_hard_merge -t 100 --human FollowerCar --robot IteratedBestResponseCar -o inf --horizon 8 -r 0 -d 5 --init_plan_scheme_r maintain_speed_lsr --init_plan_scheme_h maintain_speed_lsr -l test2
#predictreact
#[9448.815377561414, 0.0, 10087.333944334392]

