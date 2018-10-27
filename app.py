from flask import Flask, jsonify, request
from calcEthNeeded import calcEthNeeded
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'It works!'})


# validation of params for parameters
@app.route('/fill-wallet-for-gas/', methods=['GET'])
def returnQuery():
    gasNeeded = request.args.get('gas_needed')
    print(gasNeeded)
    address = request.args.get('public_address')
    speedNeeded = request.args.get('tx_speed')
    ethNeeded = calcEthNeeded(gasNeeded,speedNeeded)
    return jsonify({"gas requested": gasNeeded}, {"public address": address}, {"speed requested": speedNeeded}, {"ethNeeded in Wei": ethNeeded })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "page not found"})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
