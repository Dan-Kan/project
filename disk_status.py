import psutil
import os
import requests
import json

# List all mounted disk partitions a-la "df -h" command.

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Modified the code that (above) provided

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


def get_disks():
    disk_list = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        disk_info = {"Device": part.device,
                     "Disk size": bytes2human(usage.total),
                     "Used": bytes2human(usage.used),
                     "Free": bytes2human(usage.free),
                     "Percent used": int(usage.percent),
                     "fstype": part.fstype,
                     "Mount point": part.mountpoint}
        disk_list.append(disk_info)
    ret_dict = {"Disks" : disk_list}
    return ret_dict

'''
with open('stats.json', 'w') as outfile:
    json.dump({"Disks": get_disks()}, outfile)
'''
def write():
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["Disks"] = get_disks()["Disks"]
        f.seek(0)
        f.truncate()
        json.dump(systats, f)

def disk_runner():
    get_disks()
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["Disks"] = get_disks()["Disks"]
        f.seek(0)
        f.truncate()
        json.dump(systats, f)


'''
headers = {'Content-Type': 'application/json'}
r = requests.post("http://127.0.0.1:5000", headers=headers, json=get_disks())
'''