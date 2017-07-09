"""
Compare Bellwether XTREEs with other threshold based learners.
"""

from __future__ import print_function, division

import os
import sys
from pdb import set_trace

# Update path
root = os.path.join(os.getcwd().split('warnplan')[0], 'warnplan/warnplan')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from data.GetData import get_all_projects
from Utils.FileUtil import list2dataframe
from commons.XTREE import xtree
from Utils.StatsUtils.CrossVal import TrainTestValidate

import warnings
warnings.filterwarnings("ignore")


def planning():
    data = get_all_projects(features="processed")

    for proj, paths in data.iteritems():
        for train, test, validation in TrainTestValidate.split(paths.data):
            train = list2dataframe(train)
            test = list2dataframe(test)
            validation = list2dataframe(validation)
            set_trace()

            "Recommend changes with XTREE"

            "Have the changes been implemented?"




def apache():
    print("Apache")
    reps = dict()
    import random

    for n in xrange(1):
        for res in transfer_lessons():
            random.seed(n)  # Set a new seed for every run

            if not res.keys()[0] in reps.keys():
                reps.update({res.keys()[0]: res[res.keys()[0]]})
            else:
                reps[res.keys()[0]]["xtree_local"].extend(
                    res[res.keys()[0]]["xtree_local"])
                reps[res.keys()[0]]["xtree_bellw"].extend(
                    res[res.keys()[0]]["xtree_bellw"])
                reps[res.keys()[0]]["alves"].extend(
                    res[res.keys()[0]]["alves"])
                reps[res.keys()[0]]["shatw"].extend(
                    res[res.keys()[0]]["shatw"])
                reps[res.keys()[0]]["olive"].extend(
                    res[res.keys()[0]]["olive"])

    for n, (key, value) in enumerate(reps.iteritems()):
        print(n + 1
              , key
              , np.median(value["xtree_bellw"], axis=0)
              , np.percentile(value["xtree_bellw"], 25, axis=0)
              , np.percentile(value["xtree_bellw"], 75, axis=0)
              , np.median(value["xtree_local"], axis=0)
              , np.percentile(value["xtree_local"], 25, axis=0)
              , np.percentile(value["xtree_local"], 75, axis=0)
              , np.median(value["alves"], axis=0)
              , np.percentile(value["alves"], 25, axis=0)
              , np.percentile(value["alves"], 75, axis=0)
              , np.median(value["shatw"], axis=0)
              , np.percentile(value["shatw"], 25, axis=0)
              , np.percentile(value["shatw"], 75, axis=0)
              , np.median(value["olive"], axis=0)
              , np.percentile(value["olive"], 25, axis=0)
              , np.percentile(value["olive"], 75, axis=0)
              , sep="\t")

    set_trace()

if __name__ == "__main__":
    planning()
