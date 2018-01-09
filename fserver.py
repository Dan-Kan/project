from flask import Flask, Response, request, render_template
import json

app = Flask(__name__)

client_json = ""


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

@app.route("/draw", methods=['POST', 'GET'])
def draw_windows():
    f = json.load(open("stats.json", "r"))
    return render_template("drawin.html", window_list=f)





#@app.route("/disks", methods=['POST', 'GET'])
# def
if __name__ == '__main__':
    app.run(debug=True)
