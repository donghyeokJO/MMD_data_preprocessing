import os
import sys

sys.path.append("..")

import pandas as pd

from util import load_dir_list, load_file_list


def load_nirs(people: str, date: str, path: str):
    exp_list = load_dir_list(os.path.join(path, people, date))

    result = {
        "time_mod1": None,
        "time_mod2": None,
        "flag_mod1": None,
        "flag_mod2": None,
        "hemo_mod1": None,
        "hemo_mod2": None,
    }

    for exp in exp_list:
        if "NIRS" in exp.upper():
            file_list = load_file_list(os.path.join(path, people, date, exp))
            for file in file_list:
                if 'MOD1' in file.upper() and 'csv' in file.upper() or 'MOD2' in file.upper() and 'csv' in file.upper():
                    
