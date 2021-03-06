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
        dir = os.path.join(root, "data", data_group)

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

class CodeFeatures:
    "Code Churn Features"

    def __init__(self):
        self.projects = {}
        for file in ['ant', 'cass', 'commons', 'derby', 'jmeter', 'lucene', 'mvn', 'tomcat']:
            self.projects.update({file: _Data(data_group="code_features", data_name=file)})

class WarnFeatures:
    "Code Churn Features"

    def __init__(self):
        self.projects = {}
        for file in ['ant', 'cass', 'commons', 'derby', 'jmeter', 'lucene', 'mvn', 'tomcat']:
            self.projects.update({file: _Data(data_group="warning", data_name=file)})


def get_all_projects(features="processed"):
    all = dict()
    if features is "processed":
            all.update(Processed().projects)
    if features is "all":
            all.update(AllFeatures().projects)
    if features is "code":
            all.update(CodeFeatures().projects)
    if features is "warning":
            all.update(WarnFeatures().projects)

    return all


def _test():
    data = get_all_projects(features="processed")


if __name__ == "__main__":
    _test()
