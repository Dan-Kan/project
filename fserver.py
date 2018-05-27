from flask import Flask, Response, request, render_template, jsonify, session, redirect, g, url_for
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
import os
import ssl
from werkzeug.security import generate_password_hash, check_password_hash


def update_stats(): #Stats collection - runs in different thread
    while 1:
        window_runner()
        disk_runner()
        cpu_runner()
        ram_runner()
        time.sleep(2)


config = json.load(open("config.json"))


def start_gotty_htop():
    subprocess.call(["./gotty", "-p", "{}".format(config["local ports"]
                     [1]), "-a", "0.0.0.0", "-w", "-c", "{}:{}".format(config["username"], config["password"]), "htop"])

def start_gotty_term():
    subprocess.call(["./gotty", "-p", "{}".format(config["local ports"]
                     [2]), "-a", "0.0.0.0", "-w", "-c", "{}:{}".format(config["username"], config["password"]), "bash"])


app = Flask(__name__)
app.secret_key = os.urandom(24)

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain("myserver.crt", "myserver.key")

info_runner()

client_json = ""
stats_thread = Thread(target=update_stats, args=())
stats_thread.start()

htop_thread = Thread(target=start_gotty_htop, args=())
htop_thread.start()

term_thread = Thread(target=start_gotty_term, args=())
term_thread.start()

# subprocess.call(["./gotty" , "htop"])
# subprocess.call(["./gotty" , "-p 8081", "-w", "bash"])
# ./gotty -p 8081 -w  bash

#Login
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.pop("user", None)

        if request.form["username"] == config["username"]:
            if request.form["password"] == config["password"]:
                print("got from form: " + request.form["username"])
                session["user"] = request.form["username"]
                return redirect(url_for("live_test"))

    return render_template("login.html")


#ret stats.json
@app.route("/jstats", methods=["POST", "GET"])
def ret_json():
    if g.user:
        f = json.load(open("stats.json", "r"))
        return jsonify(f)

    return redirect(url_for("login"))

#ret config.json
@app.route("/jconfig", methods=["POST", "GET"])
def ret_config_json():
    if g.user:
        f = json.load(open("config.json", "r"))
        return jsonify(f["server"])

    return redirect(url_for("login"))

#runs close window command on server
@app.route("/closewin", methods=["POST", "GET"])
def close_win():
    if g.user:
        win_name = request.json["name"]
        print(win_name)
        cmd = "wmctrl -c " + "'" + win_name + "'"
        print("GOT COMMAND: ", cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        return "test"
    
    return redirect(url_for("login"))

#serves liveupdate.html
@app.route("/live", methods=["POST", "GET"])
def live_test():
    if g.user:
        return render_template("liveupdate.html")

    return redirect(url_for("login"))

#checks that the user is logged in before each request to server
@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]

#serves terminal.html
@app.route("/term", methods=["POST", "GET"])
def terminal_page():
    if g.user:
        return render_template("terminal.html")

    return redirect(url_for("login"))


# @app.route("/draw", methods=["POST", "GET"])
# def draw_windows():
#    f = json.load(open("stats.json", "r"))
#    return render_template("drawin.html", window_list=f)

#logout
@app.route("/logout")
def drop_session():
    session.pop("user", None)
    print("Dropped!")
    return redirect(url_for("login"))



#@app.route("/disks", methods=["POST", "GET"])
# def
#start server
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=config["local ports"][0])
    # ssl_context=context
