#!/bin/bash

python3 ../scripts/holdout-cotraining.py \
    ../Datasets/ml100k/ratings.csv \
    --results_path ../Results/holdout-cotraining-slim-funksvd.txt \
    --holdout_perc 0.8 \
    --header 0 --sep , \
    --user_key user_id --item_key item_id --rating_key rating \
    --rnd_seed 1234 \
    --recommender_1 SLIM_mt --rec_length 10 \
    --recommender_2 FunkSVD --rec_length 10 \
    --k_fold 2 \
    --number_iterations 30 \
    --number_positives 40 \
    --number_negatives 120 \
    --number_unlabeled 3000 \
    --params_1 l2_penalty=0.1,l1_penalty=0.001 \
    --params_2 num_factors=20,lrate=0.01,reg=0.0
    #--columns -> Comma separated names for every column.
    #--is_binary --make_binary --binary_th 4.0 \ -> If the dataset is binary.
