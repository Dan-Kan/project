import psutil
import os
import requests
import json
import sys


def get_cpu_percent():
    ret_dict = {"CPU": {"CPU Percent": psutil.cpu_percent(interval=1)}}
    return ret_dict


def get_cpu_termals():
    ret_dict = {}
    ret_list = []
    # acpitz = Temperature sensor near/on CPU socket. This sensor can be unreliable. NOT USING IT.
    if not hasattr(psutil, "sensors_temperatures"):
        return None
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()["coretemp"]
    if not temps:
        return None
        sys.exit("can't read any temperature")
        # print(name)
    for entry in temps:
        ret_dict[entry.label] = entry.current
    return ret_dict


def cpu_runner():
    dict = get_cpu_percent()
    if get_cpu_percent() is not None:
        dict["CPU"]["Thermals"] = get_cpu_termals()
    else:
        dict["CPU"]["Thermals"] = "Can't get temps"
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["CPU"] = dict["CPU"]
        f.seek(0)
        f.truncate()
        json.dump(systats, f)


'''
headers = {'Content-Type': 'application/json'}
r = requests.post("http://127.0.0.1:5000", headers=headers, json=get_disks())
'''
