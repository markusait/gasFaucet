from flask import Flask, jsonify, request, abort
from calcEthNeeded import calcEthNeeded
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'It works!'},{"example request": "http://localhost:8000/fill-wallet-for-gas?gas_needed=10000&tx_speed=medium&public_address=0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d"})

#handeling parameters
@app.route('/fill-wallet-for-gas/', methods=['GET'])
def returnQuery():
    # if request.method == 'GET':
    # print(request.query_string)
    #args = request.args.to_dict()
    try:
        #handeling invalid request parameter
        if not request.args.get('gas_needed'):
            raise InvalidUsage('gas_needed property incorrect', status_code=500)
        if not request.args.get('public_address'):
            raise InvalidUsage('public_address  property incorrect', status_code=500)
        if not request.args.get('tx_speed'):
            raise InvalidUsage('tx_speed property incorrect', status_code=500)

        gasNeeded = int(request.args.get('gas_needed'))
        address = request.args.get('public_address')
        speedNeeded = request.args.get('tx_speed')

        ethNeeded = calcEthNeeded(gasNeeded, speedNeeded)
        txHash = sendTransaction(ethNeeded)
        return jsonify({"gas requested": gasNeeded}, {"public address": address}, {"speed requested": speedNeeded}, {"ethNeeded in Wei": ethNeeded}, {"result:": txHash})
    #handleing exceptions
    except Exception:
        raise InvalidUsage('Invalid input', status_code=400)

#handeling invalid routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "page not found"})


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "internal server error"})

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



if __name__ == '__main__':
    app.run(debug=True, port=8000)
