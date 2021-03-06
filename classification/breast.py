#!/usr/bin/env python
#title          :breast.py
#description    :A general classification task
#author         :Henry Lin
#version        :0.0.1
#python_version :2.7.6
#================================================================================

from __future__ import division
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split, KFold
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from time import time
from sklearn.ensemble import RandomForestClassifier

SEED = 888
np.random.seed(SEED)
numFolds = 10

def main():

    # The task is to classify whether the tumor is benigh (2) or
    # malignant (4)
    dataset = pd.read_csv("data/breast.data", header=None, index_col=None)

    le = LabelEncoder()
    X = dataset.ix[:, range(1, 10)].values
    Y = le.fit_transform(dataset.ix[:, 10].values)
    kf = KFold(len(X), numFolds, shuffle=True)
    conv_X = pd.get_dummies(dataset.ix[:, range(1, 10)])

    # These are "Class objects". For each Class, find the AUC through
    # 10 fold cross validation.
    Models = [LogisticRegression, RandomForestClassifier, SVC]
    params = [{}, {}, {"probability": True}]
    for Model, param in zip(Models, params):
        total = 0
        for train_indices, test_indices in kf:

            # Get the dataset; this is the way to access values in a pandas DataFrame
            train_X = conv_X.ix[train_indices, :]; train_Y = Y[train_indices]
            test_X = conv_X.ix[test_indices, :]; test_Y = Y[test_indices]

            # Train the model, and evaluate it
            reg = Model(**param)
            reg.fit(train_X, train_Y)
            predictions = reg.predict_proba(test_X)[:, 1]
            fpr, tpr, _ = roc_curve(test_Y, predictions)
            total += auc(fpr, tpr)
        accuracy = total / numFolds
        print "AUC of {0}: {1}".format(Model.__name__, accuracy)

if __name__ == "__main__":
    main()
