#!/bin/bash

# Combination:
#  Rec1 -> item_knn with Pearson, k=50 and shrinkage = 100 and normalization
#  Rec2 -> user_knn with Pearson, k=50 and shrinkage = 100 and normalization
python3 ../scripts/holdout.py \
    ../Datasets/ml100k/ratings.csv \
    --results_path ../Results/knn-holdout.txt \
    --holdout_perc 0.8 \
    --header 0 --sep , \
    --user_key user_id --item_key item_id --rating_key rating \
    --rnd_seed 1234 \
    --recommender_1 item_knn --rec_length 10 \
    --recommender_2 user_knn --rec_length 10 \
    --number_iterations 10 \
    --number_positives 1 \
    --number_negatives 3 \
    --number_unlabeled 75 \
    --params_1 similarity=pearson,k=50,shrinkage=100,normalize=True \
    --params_2 similarity=pearson,k=50,shrinkage=100,normalize=True
    #--columns -> Comma separated names for every column.
    #--is_binary --make_binary --binary_th 4.0 \ -> If the dataset is binary.
