import psutil
import os
import requests
import json

def get_ram_percent():
    ret_list =[]
    ret_list.append({"CPU Percent" : psutil.cpu_percent(interval=1)})
    ret_dict = {"CPU" : ret_list}
    return ret_dict



def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

test = {
                'total': bytes2human(psutil.virtual_memory().total),
                'available': bytes2human(psutil.virtual_memory().available),
                'used': bytes2human(psutil.virtual_memory().used),
                'free': bytes2human(psutil.virtual_memory().free),
                'percent': psutil.virtual_memory().percent
}

print(test)

def ram_runner():
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["RAM"] = test
        f.seek(0)
        f.truncate()
        json.dump(systats, f)

ram_runner()

import psutil




print()


'''
headers = {'Content-Type': 'application/json'}
r = requests.post("http://127.0.0.1:5000", headers=headers, json=get_disks())
'''