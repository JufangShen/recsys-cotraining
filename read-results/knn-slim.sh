#!/bin/sh
# Poltecnico di Milano.
# knn-slim.sh
# Description: This file runs Co-Training with a combination of SLIM and
#               ItemKNN recommender to read results.
# Created by: Fernando Benjamín Pérez Maurera.
# Last Modified: 09/09/2017.

# The options are: -p <number> -n <number> -u <number>
# -p represents the number of positive examples to label.
# -n represents the number of negative examples to label.
# -u represents the size of the pool of unlabeled samples.
while getopts p:n:u: option
do
    case "${option}"
        in
        p) PPOSITIVES=${OPTARG};;
        n) NNEGATIVES=${OPTARG};;
        u) UNLABELED=${OPTARG};;
    esac
done

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
# Combination:
#  Rec1 -> item_knn with Cosine, k=50 and shrinkage = 100 and normalization
#  Rec2 -> SLIM with Pearson, k=50 and shrinkage = 100 and normalization
python3 ../scripts/read_results.py \
    ../Datasets/ml10m/ratings.csv \
    --results_path ../Results/knn-slimmt-3/ \
    --results_file holdout-knn-slim-50.csv \
    --holdout_perc 0.8 \
    --header 0 --sep , \
    --user_key user_id --item_key item_id --rating_key rating \
    --rnd_seed 1234 \
    --recommender_1 item_knn --rec_length 10 \
    --recommender_2 SLIM_mt --rec_length 10 \
    --number_iterations 50 \
    --number_positives $PPOSITIVES \
    --number_negatives $NNEGATIVES \
    --number_unlabeled $UNLABELED \
    --params_1 similarity=adj-cosine,k=350,shrinkage=0,normalize=True \
    --params_2 l2_penalty=0.1,l1_penalty=0.001 \
    --to_read label_comparison,numberlabeled \
    --make_pop_bins
    #--columns -> Comma separated names for every column.
    #--is_binary --make_binary --binary_th 4.0 \ -> If the dataset is binary.
