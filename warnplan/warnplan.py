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
from data.get_data import get_all_projects
from commons.utils.FileUtil import list2dataframe
from planners.xtree import xtree
from commons.utils.StatsUtils.CrossVal import TrainTestValidate

import warnings
warnings.filterwarnings("ignore")


def planning():
    data = get_all_projects(features="processed")
    results = dict()
    for proj, paths in data.iteritems():
        results.update({proj: []})
        for train, test, validation in TrainTestValidate.split(paths.data):

            "Convert to pandas type dataframe"
            train = list2dataframe(train)
            test = list2dataframe(test)
            validation = list2dataframe(validation)

            "Recommend changes with XTREE"
            new = xtree(train[train.columns[1:]], test)

            """
            Have the changes been implemented?" 
            """

            "Create a smaller dframe of all closed issues in validation set"
            closed_in_validation = validation[validation['category'].isin([0])]

            "Group the smaller dframe and the patched dframe by their file names"
            modules = list(set(closed_in_validation["Name"].tolist()))


            "Find the deltas between patched and smaller validation dframe"
            heeded = []
            for module_name in modules:
                count = []
                module_name_new = new[new["Name"].isin([module_name])]
                module_name_val = closed_in_validation[closed_in_validation["Name"].isin([module_name])]
                for col_name in module_name_val.columns[1:-1]:
                    aa = module_name_new[col_name]
                    bb = module_name_val[col_name]
                    try:
                        ranges = sorted(eval(aa.values.tolist()[0]))
                        count.append(any([abs(ranges[0]) <= bbb <= abs(ranges[1]) for bbb in bb.tolist()]))
                    except TypeError:
                        count.append(any([bbb == aa.values[0] for bbb in bb.tolist()]))
                    except IndexError:
                        pass
                if len(count) > 0:
                    heeded.append(sum(count)/len(count))
        results[proj]= heeded

        "Print output"
        percentiles = np.percentile(results[proj], [25, 50, 75])
        print("{}\t{:0.2f}\t{:0.2f}\t{:0.2f}".format(proj[:5], percentiles[0], percentiles[1], percentiles[2]))

if __name__ == "__main__":
    planning()
