from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def get_data():
    print('Recieved from client: {}'.format(request.data))
    return Response(request.data)

if __name__ == '__main__':
    app.run(debug=True)