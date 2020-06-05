import argparse, itertools, pickle, sys
import pandas as pd
from multiprocessing import Pool
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# import from this project
from data import Data
from model import Model

DATASETS = ["sea", "breastw", "sonar", "heart", "planes", "house16", "cal_housing", "houses", "house8",
            "fried", "letter", "spectf_test", "austr", "spectf", "click1", "click2", "click3", "skin",
            "creditcard", "numerai"]
MODELS = ["SVM", "ANN", "NB", "LOGREG", "ADA", "RF", "DT", "KNN", "BAG-DT"]

def run_single(args):
    """Run an experiment on a single model."""
    im, ds, size = args # un-pack the argument tuple
    d = Data(ds, size)
    m = Model(ds, im, only_beta=False, only_log=False)
    try:
        if im == "DT":
            im_res, _ = m.run(d, DecisionTreeClassifier(min_samples_leaf=10))
        elif im == "NB":
            im_res, _ = m.run(d, GaussianNB())
        elif im == "SVM":
            im_res, _ = m.run(d, SVC())
        elif im == "RF":
            im_res, _ = m.run(d, RandomForestClassifier())
        elif im == "KNN":
            im_res, _ = m.run(d, KNeighborsClassifier())
        elif im == "LOGREG":
            im_res, _ = m.run(d, LogisticRegression())
        elif im == "BAG-DT":
            im_res, _ = m.run(d, BaggingClassifier(DecisionTreeClassifier()))
        elif im == "ADA":
            im_res, _ = m.run(d, AdaBoostClassifier())
        elif im == "ANN":
            im_res, _ = m.run(d, MLPClassifier())
    except Exception as err:
        print("ERROR: Didn't manage with model " + im + ": ", err)
        return im, err
    with open('results/models/may30_%s_%s.pkl' % (ds, im), 'wb') as output:
        pickle.dump(m, output, pickle.HIGHEST_PROTOCOL)
    print("SUCCESS with model " + im)
    return im, im_res # return a mapping from model name to the results

def run_all(size, ds):
    """Run all experiments of a given training size and dataset, using all models"""
    args = list(itertools.product(
        MODELS,
        [ ds ],
        [ size ]
    )) # cartesian product of configurations
    with Pool() as pool:
        res = dict(pool.imap_unordered(run_single, args))
    return {ds: res}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run analysis pipeline for all models')
    parser.add_argument('--size', dest='size', help='Size for the training set (e.g., 100, 1000, or 3000)', type=int)
    parser.add_argument('--dataset', dest='dataset', help=f'The dataset identifier', choices=DATASETS)
    args = parser.parse_args()

    res = run_all(args.size, args.dataset)
    pickle.dump(res, open("results/res_%s_%s.pickle" % (args.size, args.dataset), "wb"))
