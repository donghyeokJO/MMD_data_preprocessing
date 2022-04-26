import os


def load_dir_list(path) -> list:
    dir_list = []

    for entry in os.scandir(path):
        if entry.is_dir():
            dir_list.append(entry.name)

    return dir_list


def load_file_list(path) -> list:
    file_list = []

    for entry in os.scandir(path):
        if entry.is_file():
            file_list.append(entry.name)

    return file_list
