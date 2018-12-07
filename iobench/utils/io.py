import json
import os
import datetime


def get_time_str():
    """
    returs current time formatted nicely
    """
    time_now = datetime.datetime.now()
    str_time = time_now.strftime("%y.%m.%d_%H.%M.%S")
    return str_time


def save_data_to_json(data, name_file):
    """
    saves dictionary to json files
    creates dirs of they do not exist
    """
    path = os.path.realpath(os.path.dirname(name_file))
    os.makedirs(path, exist_ok=True)
    s = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
    f = open(name_file, 'w')
    print(s, file=f)
    f.close()
