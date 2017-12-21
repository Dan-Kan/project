from flask import Flask, Response, request, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def get_data():
    print('Recieved from client: {}'.format(request.get_data()))
    global client_json
    if(request.get_json()):
        client_json = request.get_json()
    return "<h1>Hi!</h1>"


@app.route("/json", methods=['POST', 'GET'])
def get_json():
    print("IN /json")
    print()
    if(client_json):
        print(client_json)
        return client_json
    else:
        return "DIDNT GET JSON"


if __name__ == '__main__':
    app.run(debug=True)
