import pandas as pd
import numpy as np

from constants import TRIGGER_PATH


def trigger_switch(people="강나은", date="basal", data: dict = None):
    trigger_ = pd.read_excel(TRIGGER_PATH, header=0)

    tcd_switch = False

    cur_trigger_ = trigger_[(trigger_["Subject"] == people) & (trigger_["Day"] == date)]

    surgery = cur_trigger_["surgery"].values[0]

    trigger = list(
        map(lambda x: x.strftime("%H:%M:%S"), cur_trigger_.iloc[:, 6:].values[0])
    )

    time = np.array(data.get("ori_time"))

    sep = []

    for i in range(len(trigger)):
        tmp = list(np.where(time >= trigger[i]))
        if len(tmp) == 0:
            if i == len(trigger):
                sep[i] = len(time)
        else:
            sep.append(tmp[0][0])

    return tcd_switch, surgery, sep, trigger


if __name__ == "__main__":
    trigger_switch()
