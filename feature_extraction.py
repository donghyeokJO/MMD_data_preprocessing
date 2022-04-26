import os

from constants import DATA_PATH, DATA_PATH_ADD, OUTPUT_PATH
from util import load_dir_list
from data_preprocess import *


class MMDFeatureExtraction:
    total_result: list
    window_update: float
    NIRS_freq: float
    fs: int
    file_list_MMD: list
    file_list_MMD_ADD: list
    fina_tcd: dict
    fina_tcd_add: dict
    nirs: dict
    nirs_add: dict

    def __init__(self):
        self.total_result = [
            "subject",
            "day",
            "mod",
            "region",
            "trials",
            "Phase",
            "mean_abp",
        ]

        self.window_update = 1 / 60
        self.NIRS_freq = 8.138 * 4
        self.fs = 200

        self.file_list_MMD = load_dir_list(DATA_PATH)
        self.file_list_MMD_ADD = load_dir_list(DATA_PATH_ADD)

        self.file_list_per_people = dict(
            map(
                lambda x: (x, load_dir_list(os.path.join(DATA_PATH, x))),
                self.file_list_MMD,
            )
        )
        self.file_list_add_per_people = dict(
            map(
                lambda x: (x, load_dir_list(os.path.join(DATA_PATH_ADD, x))),
                self.file_list_MMD_ADD,
            )
        )

        self.fina_tcd = {}
        self.fina_tcd_add = {}

        self.nirs = {}
        self.nirs_add = {}

    def load_fina_tcd(self):
        print("Data load started - MMD")

        for people in self.file_list_per_people:
            people_split = people.split("-")[-1]
            self.fina_tcd[people_split] = {}
            for date in self.file_list_per_people[people]:
                date_ = date.replace("#", "")
                self.fina_tcd[people_split][date_] = load_fina_tcd(
                    people, date, DATA_PATH
                )

        print("Data loaded - MMD")

        print("Data load start - MMD ADD")

        for people in self.file_list_add_per_people:
            people_split = people.split("-")[-1]
            self.fina_tcd_add[people_split] = {}
            for date in self.file_list_add_per_people[people]:
                date_ = date.replace("#", "")
                self.fina_tcd_add[people_split][date_] = load_fina_tcd(
                    people, date, DATA_PATH_ADD
                )

        print("Data loaded - MMD ADD")

    @staticmethod
    def swap(a, b):
        tmp = b
        b = a
        a = tmp

        return a, b

    @staticmethod
    def cut_back(data, first_index, last_index):
        return data[first_index : last_index + 1]

    def get_trigger_switch(self):
        for people in self.fina_tcd:
            for date in self.fina_tcd[people]:
                tcd_switch, surgery, sep, trigger = trigger_switch(
                    people, date, self.fina_tcd[people][date]
                )
                if tcd_switch:
                    (
                        self.fina_tcd_add[people][date]["TCD_L"],
                        self.fina_tcd_add[people][date]["TCD_R"],
                    ) = self.swap(
                        self.fina_tcd_add[people][date]["TCD_L"],
                        self.fina_tcd_add[people][date]["TCD_R"],
                    )
                self.fina_tcd_add[people][date]["Fina"] = self.cut_back(
                    self.fina_tcd_add[people][date]["Fina"], sep[0], sep[-1]
                )
                self.fina_tcd_add[people][date]["TCD_L"] = self.cut_back(
                    self.fina_tcd_add[people][date]["TCD_L"], sep[0], sep[-1]
                )
                self.fina_tcd_add[people][date]["TCD_R"] = self.cut_back(
                    self.fina_tcd_add[people][date]["TCD_R"], sep[0], sep[-1]
                )
                subtract_ = sep[0]
                sep = [x - subtract_ for x in sep]

        for people in self.fina_tcd_add:
            for date in self.fina_tcd_add[people]:
                tcd_switch, surgery, sep, trigger = trigger_switch(
                    people, date, self.fina_tcd_add[people][date]
                )
                if tcd_switch:
                    (
                        self.fina_tcd_add[people][date]["TCD_L"],
                        self.fina_tcd_add[people][date]["TCD_R"],
                    ) = self.swap(
                        self.fina_tcd_add[people][date]["TCD_L"],
                        self.fina_tcd_add[people][date]["TCD_R"],
                    )
                self.fina_tcd_add[people][date]["Fina"] = self.cut_back(
                    self.fina_tcd_add[people][date]["Fina"], sep[0], sep[-1]
                )
                self.fina_tcd_add[people][date]["TCD_L"] = self.cut_back(
                    self.fina_tcd_add[people][date]["TCD_L"], sep[0], sep[-1]
                )
                self.fina_tcd_add[people][date]["TCD_R"] = self.cut_back(
                    self.fina_tcd_add[people][date]["TCD_R"], sep[0], sep[-1]
                )
                subtract_ = sep[0]
                sep = [x - subtract_ for x in sep]

    def load_nirs(self):
        print("Data(NIRS) load started - MMD")

        for people in self.file_list_per_people:
            people_split = people.split("-")[-1]
            self.fina_tcd[people_split] = {}
            for date in self.file_list_per_people[people]:
                date_ = date.replace("#", "")
                self.fina_tcd[people_split][date_] = load_nirs(people, date, DATA_PATH)
                break
            break

        print("Data(NIRS) loaded - MMD")


if __name__ == "__main__":
    feature_extraction = MMDFeatureExtraction()
    # feature_extraction.load_fina_tcd()
    # feature_extraction.get_trigger_switch()
    feature_extraction.load_nirs()
