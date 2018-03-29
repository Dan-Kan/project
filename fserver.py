from flask import Flask, Response, request, render_template, jsonify
import json
import threading
from disk_status import disk_runner
from getwindows import window_runner
from cpu_stats import cpu_runner
from ram_status import ram_runner
import time
from threading import Thread
import subprocess
from top_bar import info_runner


def update_stats():
  while 1:
    window_runner()
    disk_runner()
    cpu_runner()
    ram_runner()
    time.sleep(2)

def start_gotty():
    subprocess.call(["./gotty", "-a", "0.0.0.0", "htop"])
    subprocess.call(["./gotty", "-p", "8081", "-a", "0.0.0.0", "-w", "bash"])

app = Flask(__name__)

info_runner()

client_json = ""

thread = Thread(target = update_stats, args = ( ))
thread.start()

thread = Thread(target = start_gotty, args = ( ))
thread.start()

#subprocess.call(["./gotty" , "htop"])
#subprocess.call(["./gotty" , "-p 8081", "-w", "bash"])
#./gotty -p 8081 -w  bash
def merge_json(jwin, jdisks):
    combined = json.dumps(jwin + jdisks)
    print(combined)
    return json.dumps(combined)


@app.route("/", methods=['POST', 'GET'])
def get_data():
    print('Recieved from client: {}'.format(request.get_json()))
    global client_json
    if(request.get_json() and client_json == ""):
        client_json = request.get_json()
    elif(request.get_json()):
        client_json = merge_json(client_json, request.get_json())
        print()
        print()
        print("client_json: " + client_json)
    return "<h1>Hi!</h1>"


@app.route("/win", methods=['POST', 'GET'])
def get_json():
    print("IN /win")
    print()
    f = json.load(open("stats.json", "r"))
    return render_template("windowtable.html", window_list=f)

@app.route("/jstats", methods=['POST', 'GET'])
def ret_json():
    f = json.load(open("stats.json", "r"))
    return jsonify(f)

@app.route("/closewin", methods=['POST', 'GET'])
def close_win():
    win_name = request.json["name"];
    print(win_name)
    cmd = "wmctrl -c " + win_name
    print("GOT COMMAND: ", cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return "test"

@app.route("/live", methods=['POST', 'GET'])
def live_test():
    #print(subprocess.getoutput("pwd"))
    #subprocess.call(["./", "gotty", "htop"])
    return render_template("liveupdate.html")

@app.route("/term", methods=['POST', 'GET'])
def terminal_page():
    #print(subprocess.getoutput("pwd"))
    #subprocess.call(["./", "gotty", "htop"])
    return render_template("terminal.html")

@app.route("/draw", methods=['POST', 'GET'])
def draw_windows():
    f = json.load(open("stats.json", "r"))
    return render_template("drawin.html", window_list=f)





#@app.route("/disks", methods=['POST', 'GET'])
# def
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
