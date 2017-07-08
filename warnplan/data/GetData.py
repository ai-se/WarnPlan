import os
import sys
from pdb import set_trace
from glob import glob

root = os.path.join(os.getcwd().split('warnplan')[0], 'warnplan/warnplan')
if root not in sys.path:
    sys.path.append(root)


class _Data:
    """Hold training and testing data.dat"""

    def __init__(self, data_group, data_name):
        dir = os.path.join(root, "data/processed/")

        self.data = glob(os.path.abspath(os.path.join(dir, data_name, "*.csv")))


class Processed:
    "Processed data (top features only)"

    def __init__(self):
        self.projects = {}
        for file in ['ant', 'cass', 'commons', 'derby', 'jmeter', 'lucene', 'mvn', 'tomcat']:
            self.projects.update({file: _Data(data_group="processed", data_name=file)})

class AllFeatures:
    "All Features"

    def __init__(self):
        self.projects = {}
        for file in ['ant', 'cass', 'commons', 'derby', 'jmeter', 'lucene', 'mvn', 'tomcat']:
            self.projects.update({file: _Data(data_group="all_features", data_name=file)})


def get_all_projects(features="processed"):
    all = dict()
    if features is "processed":
            all.update({Processed.__name__.lower(): Processed().projects})
    if features is "all":
            all.update({AllFeatures.__name__.lower(): AllFeatures().projects})

    return all


def _test():
    data = get_all_projects(features="processed")


if __name__ == "__main__":
    _test()
