import psutil
import os
import requests
import json

def get_cpu_percent():
    ret_list =[]
    ret_list.append({"CPU Percent" : psutil.cpu_percent(interval=1)})
    ret_dict = {"CPU" : ret_list}
    return ret_dict

def cpu_runner():
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["CPU"] = get_cpu_percent()["CPU"]
        f.seek(0)
        f.truncate()
        json.dump(systats, f)


'''
headers = {'Content-Type': 'application/json'}
r = requests.post("http://127.0.0.1:5000", headers=headers, json=get_disks())
'''