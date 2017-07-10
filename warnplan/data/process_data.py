from __future__ import print_function
import re, os, sys
import pandas as pd
from glob2 import glob
from pdb import set_trace

if __name__ == "__main__":
    all_features = "totalFeatures.csv"
    all_labels = "labelAll.csv"
    source_code = "sourceCode"

    code_features_ids = ["F55", "F41","F40","F43","F42","F45","F44","F140","F47","F141","F46","F142","F49","F143","F48"
        ,"F126","F127","F128","F129","F50","F52","F51","F36","F130","F35","F131","F38","F132","F37","F133","F134","F39"
        ,"F135","F136","F137","F138","F139", "category"]

    selected_label_id = ["F55", "F116", "F115", "F117", "F121",
                         "F110", "F64", "F104", "F101", "F68",
                         "F72", "F22", "F77", "category"]

    selected_label_tag = ["wCtx_Method", "wCtx_File", "defect_likely",
                          "change_remove_rate", "wCtx_Warning", "file_depth",
                          "method_depth", "num_classes", "package_size",
                          "comment_code_ratio", "num_developers", "file_creation_revisions",
                          "param_signature", "warn_prio", "warn_lifetime"]
    features = [os.path.abspath(d) for d in glob("Raw/*/**") \
                if "totalFeatures" in d]
    source_code_features = []
    labels = [os.path.abspath(d) for d in glob("Raw/*/**") \
              if "labelAll" in d]
    for p, l in zip(features, labels):
        feature_dframe = pd.read_csv(p)
        label_dframe = pd.read_csv(l, header=None)
        dframe = feature_dframe[selected_label_id]
        code_dframe = pd.read_csv(re.sub("totalFeatures", "sourceCode", p))
        code_dframe_full = pd.concat([feature_dframe["F55"], code_dframe[code_dframe.columns[:-1]], feature_dframe["category"]], axis=1)
        warn_dframe = pd.read_csv(re.sub("totalFeatures", "warningCombine", p))
        warn_dframe_full = pd.concat([feature_dframe["F55"], code_dframe[code_dframe.columns[:-1]], feature_dframe["category"]], axis=1)


        # "Only select features"
        # if not os.path.isdir(re.sub("Raw", "processed",
        #                             "/".join(p.split("/")[:-2]))):
        #     os.mkdir(re.sub("Raw", "processed", "/".join(p.split("/")[:-2])))
        #
        # dframe.to_csv(re.sub("Raw", "processed", "/".join(
        #     p.split("/")[:-1]) + ".csv"), index=False,
        #               header=["Name"]+selected_label_id[1:])

        # set_trace()
        # "Code features"
        # if not os.path.isdir(re.sub("Raw", "code_features",
        #                     "/".join(p.split("/")[:-2]))):
        #     os.mkdir(re.sub("Raw", "code_features", "/".join(p.split("/")[:-2])))
        #
        # code_dframe_full.to_csv(re.sub("Raw", "code_features", "/".join(p.split("/")[:-1])+".csv"), index=False)

        "Warnings"
        if not os.path.isdir(re.sub("Raw", "code_features",
                            "/".join(p.split("/")[:-2]))):
            os.mkdir(re.sub("Raw", "warning", "/".join(p.split("/")[:-2])))

        warn_dframe_full.to_csv(re.sub("Raw", "warning", "/".join(p.split("/")[:-1])+".csv"), index=False)

        # "All features"
        # if not os.path.isdir(re.sub("Raw", "all_features",
        #                     "/".join(p.split("/")[:-2]))):
        #     os.mkdir(re.sub("Raw", "all_features", "/".join(p.split("/")[:-2])))
        # # set_trace()
        # feature_dframe.to_csv(re.sub("Raw", "all_features", "/".join(p.split("/")[:-1])+".csv"), index=False)
