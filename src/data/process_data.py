from __future__ import print_function
import os, sys
import pandas as pd
from glob2 import glob
from pdb import set_trace


if __name__ == "__main__":
    all_features = "totalFeatures.csv"
    all_labels = "labelAll.csv"
    selected_label_id = ["F107", "F108", "F112", "F110",
                         "F106", "F21", "F23", "F25", "F31",
                         "F18", "F16", "F72", "F91", "F99"]
    files = glob("Raw")
    set_trace()
