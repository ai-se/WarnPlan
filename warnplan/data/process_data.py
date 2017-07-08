from __future__ import print_function
import re, os, sys
import pandas as pd
from glob2 import glob
from pdb import set_trace

if __name__ == "__main__":
    all_features = "totalFeatures.csv"
    all_labels = "labelAll.csv"
    selected_label_id = ["F116", "F115", "F117", "F121",
                         "F110", "F64", "F104", "F101", "F68",
                         "F72", "F22", "F77"]
    selected_label_tag = ["wCtx_Method", "wCtx_File", "defect_likely",
            "change_remove_rate", "wCtx_Warning", "file_depth",
            "method_depth", "num_classes", "package_size",
            "comment_code_ratio", "num_developers", "file_creation_revisions",
            "param_signature", "warn_prio", "warn_lifetime"]
    features = [os.path.abspath(d) for d in glob("Raw/*/**") \
                             if "totalFeatures" in d]
    labels = [os.path.abspath(d) for d in glob("Raw/*/**") \
                             if "labelAll" in d]
    for p, l in zip(features, labels):
        feature_dframe = pd.read_csv(p)
        label_dframe = pd.read_csv(l, header=None)
        dframe=pd.concat([feature_dframe[selected_label_id], label_dframe[label_dframe.columns[0]]], axis=1)
        # dframe_all=pd.concat([feature_dframe, label_dframe[label_dframe.columns[0]]], axis=1)

        # "Only select features"
        # if not os.path.isdir(re.sub("Raw", "processed",
        #                     "/".join(p.split("/")[:-2]))):
        #     os.mkdir(re.sub("Raw", "processed", "/".join(p.split("/")[:-2])))
        # dframe.to_csv(re.sub("Raw", "processed", "/".join(
        #                 p.split("/")[:-1])+".csv"), index=False,
        #                 header=selected_label_id+["status"])
        "All features"
        if not os.path.isdir(re.sub("Raw", "all_features",
                            "/".join(p.split("/")[:-2]))):
            os.mkdir(re.sub("Raw", "all_features", "/".join(p.split("/")[:-2])))
        # set_trace()
        feature_dframe.to_csv(re.sub("Raw", "all_features", "/".join(
                        p.split("/")[:-1])+".csv"), index=False,
                        header=feature_dframe.columns.tolist()[:-1]+["status"])
