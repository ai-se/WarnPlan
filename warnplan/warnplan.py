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

            "Convert to pandas type dataframe"
            train = list2dataframe(train)
            test = list2dataframe(test)
            validation = list2dataframe(validation)

            "Recommend changes with XTREE"
            new, changes = xtree(train[train.columns[1:]], test)

            """
            Have the changes been implemented?" 
            """

            "Create a smaller dframe of all closed issues in validation set"
            closed_in_validation = validation[validation['category'].isin([0])]

            "Group the smaller dframe and the patched dframe by their file names"
            modules = list(set(closed_in_validation["Name"].tolist()))

            for module_name in modules:
                module_name_val = closed_in_validation[closed_in_validation["Name"].isin([module_name])]
                module_name_new = new[new["Name"].isin([module_name])]
                set_trace()
            "Find the deltas between patched and smaller validation dframe"

if __name__ == "__main__":
    planning()
