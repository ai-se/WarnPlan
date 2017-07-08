from __future__ import print_function, division

from pdb import set_trace

import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import LeaveOneOut


class CrossValidation:
    def __init__(self):
        pass

    @classmethod
    def split(cls, dframe, ways=5):
        col = dframe.columns
        X = dframe
        y = dframe[dframe.columns[-1]]
        skf = StratifiedKFold(n_splits=ways, shuffle=True)
        for train_idx, test_idx in skf.split(X, y):
            yield pd.DataFrame(X.values[train_idx], columns=col), \
                  pd.DataFrame(X.values[test_idx], columns=col)


class LeaveOneOutValidation:
    def __init__(self):
        pass

    @classmethod
    def split(cls, dframe, ways=5):
        col = dframe.columns
        X = dframe
        y = dframe[dframe.columns[-1]]
        loo = LeaveOneOut()
        for train_idx, test_idx in loo.split(X, y):
            yield pd.DataFrame(X.values[train_idx], columns=col), \
                  pd.DataFrame(X.values[test_idx], columns=col)
