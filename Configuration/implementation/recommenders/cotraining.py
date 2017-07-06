'''
Politecnico di Milano.
co-training.py

Description: This file contains the definition and implementation of a
             Co-Training environment to train, boost and evaluate different recommenders

Modified by Fernando Pérez.

Last modified on 25/03/2017.
'''

import random as random
import logging
from datetime import datetime as dt

import numpy as np
import scipy as sp

import sys
import pdb

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

class CoTraining(object):
    """ CO-TRAINING environment for RecSys"""

    def __init__(self, rec_1, rec_2, eval_obj, n_iters = 30, n_labels = 10, p_most = 1, n_most = 3, seed=1024):
        '''
            Args:
                * rec_1: A Recommender Class object that represents the first
                         recommender.
                * rec_2: A Recommender Class object that represents the second
                         recommender.
                * eval_obj: An Evaluation Class object that represents the evaluation
                            metrics for the recommender1.
                * n_iters: Represents the number of Co-Training iterations.
                * n_labels: The number of elements to label in each Co-Training
                            iteration.
        '''
        super(CoTraining, self).__init__()
        self.rec_1 = rec_1
        self.rec_2 = rec_2
        self.eval = eval_obj
        self.n_iters = n_iters
        self.n_labels = n_labels
        self.p_most = p_most
        self.n_most = n_most
        self.seed = seed

    def short_str(self):
        return "CoTraining(Rec1={},Rec2={},Iter={})".format(
            self.rec_1.short_str(),self.rec_2.short_str(),self.n_iters)

    def __str__(self):
        return "CoTrainingEnv(Rec1={},Rec2={},Iterations={})".format(
            self.rec_1.__str__(), self.rec_2.__str__(), self.n_iters)

    def fit(self, X1, eval_iter = False):
        '''
            Depending of the Co-Training approach, you can have two views or
            use different learners, in the case of X2 == None, it's supposed
            that the same dataset will be used,

            Args:
                X_unlabeled: Set of X_unlabeled user/item pairs that doesn't have
                             a rating. It must be a DOK matrix.
                X1: Represents the training dataset to be used for the first
                    recommender. It must be a DOK matrix.
                X2: Represents the training dataset to be used for the second
                    recommender. It must be a DOK matrix.
                eval_iter: Tells if we need to evaluate each recommender and the
                           joint at each iteration.

        '''
        # self.eval_aggr.recommender = self
        nusers, nitems = X1.shape
        rng = np.random.RandomState(self.seed)

        # Create the pool of examples.
        # Using a DoK matrix to have a A[row[k], col[k]] = Data[k] representation
        # without having an efficiency tradeoff.
        u_prime = sp.sparse.dok_matrix((nusers,nitems), dtype=np.int32)

        # Feed U' with unlabeled samples.
        i = 0
        while (i < self.n_labels):
            rnd_user = rng.randint(0, high=nusers, dtype=np.int32)
            rnd_item = rng.randint(0, high=nitems, dtype=np.int32)
            if (X1.get((rnd_user,rnd_item),0) == 0.0): # TODO: user better precision (machine epsilon instead of == 0.0)
                u_prime.update({(rnd_user,rnd_item): 1})
                i += 1

        # Training set for Rec2.
        X2 = X1.copy()

        # Co-Training iterations begin here.
        for i_iter in range(self.n_iters):
            logger.info(("Iteration: {}".format(i_iter)))

            try:
                logger.info('\tRecommender: {}'.format(self.rec_1))
                tic = dt.now()
                logger.info('\t\tTraining started for recommender: {}'.format(self.rec_1))
                self.rec_1.fit(X1)
                logger.info('\t\tTraining completed in {} for recommender: {}'.format(dt.now() - tic, self.rec_1))
            except:
                logger.info('Could not fit the recommender 1: {}'.format(sys.exc_info()[0]))

            # try:
            logger.info('\tRecommender: {}'.format(self.rec_2))
            tic = dt.now()
            logger.info('\t\tTraining started for recommender: {}'.format(self.rec_2))
            self.rec_2.fit(X2)
            logger.info('\t\tTraining completed in {} for recommender: {}'.format(dt.now() - tic, self.rec_2))
            # except:
            #     logger.info('Could not fit the recommender 2: {}'.format(sys.exc_info()[0]))


            # Evaluate the recommenders in this iteration.
            logger.info('\tEvaluating both recommenders.')
            try:
                self.eval.eval(self.rec_1, self.rec_2)
                # self.eval2.eval(X2)
                # self.eval_aggr.eval(X1) # TODO: change this.
                self.eval.log_by_index(i_iter, self.rec_1, self.rec_2)
                # self.eval2.log_by_index(i_iter)
                # self.eval_aggr.log_by_index(i_iter)
            except:
                logger.info('Could not evaluate both recomemnders: {}'.format(sys.exc_info()[0]))


            # Label positively and negatively examples from U' for both recommenders.
            logger.info('\tLabeling new items.')
            unlabeled = u_prime.keys()
            unl1 = list(unlabeled)
            unl2 = list(unlabeled)
            try:
                labeled1 = self.rec_1.label(unlabeled_list=unl1, binary_ratings=False, exclude_seen=True, p_most=self.p_most, n_most=self.n_most)
            except:
                logger.info('Could not label new items for recomemnder 1: {}'.format(sys.exc_info()[0]))
            try:
                labeled2 = self.rec_2.label(unlabeled_list=unl2, binary_ratings=False, exclude_seen=True, p_most=self.p_most, n_most=self.n_most)
            except:
                logger.info('Could not label new items for recomemnder 2: {}'.format(sys.exc_info()[0]))

            # Add the labeled examples from recommender1 into T2. (and eliminate them from U' as they aren't X_unlabeled anymore).
            for user_idx, item_idx, label in labeled1:
                X2.update({(user_idx,item_idx): label})
                u_prime.update({(user_idx,item_idx): 0})

            # Add the labeled examples from recommender2 into T1. (and eliminate them from U' as they aren't X_unlabeled anymore).
            for user_idx, item_idx, label in labeled2:
                X1.update({(user_idx,item_idx): label})
                u_prime.update({(user_idx,item_idx): 0})

            # Replenish U' with 2*p + 2*n samples from U.
            i = 0
            while (i < (len(labeled1) + len(labeled2)) ):
                rnd_user = rng.randint(0, high=nusers, dtype=np.int32)
                rnd_item = rng.randint(0, high=nitems, dtype=np.int32)
                if (X1.get((rnd_user,rnd_item),0) == 0.0 and X2.get((rnd_user,rnd_item),0) == 0.0): # TODO: user better precision (machine epsilon instead of == 0.0)
                    u_prime.update({(rnd_user,rnd_item): 1})
                    i += 1

    def recommend(self, user_id, n=None, exclude_seen=True):
        scores1 = self.rec_1.user_score(user_id=user_id)
        scores2 = self.rec_2.user_score(user_id=user_id)
        scores = (scores1 + scores2) / 2.0 # Averaging the score.

        # rank items
        ranking = scores.argsort()[::-1]
        if exclude_seen:
            ranking = self.rec_1._filter_seen(user_id, ranking)
        return ranking[:n]

    def predict(self, user_id, rated_indices):
        predict1 = self.rec_1.predict(user_id, rated_indices)
        predict2 = self.rec_2.predict(user_id, rated_indices)

        predict = (predict1 + predict2) / 2.0 # Averaging the scores.
        return predict


    def random_user_sample_random_item_sample(self, dataset, n_samples = 75):
        '''
            Returns a set of randomly choosen user/item pairs which doesn't have
            rating.
        '''
        nusers, nitems = dataset.shape
        i_sample = 0
        random_pop = set()
        while (i_sample < n_samples):
            rnd_user = np.random.randint(0, high=nusers, dtype=np.int32)
            rnd_item = np.random.randint(0, high=nitems, dtype=np.int32)
            if (dataset[rnd_user, rnd_item] == 0.0): # TODO: user better precision (machine epsilon instead of == 0.0)
                random_pop.add( (rnd_user, rnd_item) )
                i_sample +=1
        return random_pop
