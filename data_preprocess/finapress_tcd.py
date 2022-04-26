import os
import sys

sys.path.append("..")

import pandas as pd

from util import load_dir_list, load_file_list


def load_fina_tcd(people: str, date: str, path: str):
    exp_list = load_dir_list(os.path.join(path, people, date))

    result = {
        "ori_time": None,
        # "fina_TCD": None,
        "Fina": None,
        "TCD_L": None,
        "TCD_R": None,
    }

    for exp in exp_list:
        if "TCD" in exp.upper():
            file_list = load_file_list(os.path.join(path, people, date, exp))
            # print(f"{people}: {file_list}")
            for file in file_list:
                if "200HZ" in file.upper():
                    file_path = os.path.join(path, people, date, exp, file)
                    data = pd.read_csv(file_path, header=None)

                    data = data.fillna(0)

                    result["ori_time"] = list(
                        map(lambda x: x[10:], data.iloc[:, 0].values)
                    )

                    data_part = data.iloc[:, 1:]
                    result["Fina"] = list(data_part.iloc[:, 1].values)
                    result["TCD_R"] = list(data_part.iloc[:, 2].values)
                    result["TCD_L"] = list(data_part.iloc[:, 3].values)

                break
            break

    # print(result["ori_time"])
    return result
