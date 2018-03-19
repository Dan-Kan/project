import psutil
import os
import requests
import json
import subprocess

#ORDER OF UNAME COMMANDS:
    #uname -n
    #uname -sro
    #uname -m

#TO GET PUBLIC IP ADDR: curl ipecho.net/plain ; echo
pub_ip = subprocess.getoutput("wget -qO- http://ipecho.net/plain ; echo")

#TO GET PRIMARY IP ADDR: ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'
prim_ip = subprocess.getoutput("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'")

machine_name = subprocess.getoutput("uname -n")
os_info = subprocess.getoutput("uname -sro")
arc = subprocess.getoutput("uname -m")

curr_user = subprocess.getoutput("whoami")

print(machine_name, os_info, arc) #prefect
print (curr_user)
print(prim_ip)
print(pub_ip)

def info_runner():
    with open("stats.json", "r+") as f:
        systats = json.load(f)
        # update json here
        systats["MACHINE_INFO"] = machine_name + " " + os_info + " " + arc + " " + curr_user
        systats["IP_ADDR"] = prim_ip + " / " + pub_ip
        f.seek(0)
        f.truncate()
        json.dump(systats, f)

#info_runner()

'''
headers = {'Content-Type': 'application/json'}
r = requests.post("http://127.0.0.1:5000", headers=headers, json=get_disks())
'''