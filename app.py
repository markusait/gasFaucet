from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'It works!'})


# validation of params for parameters
@app.route('/fill-wallet-for-gas/', methods=['GET'])
def returnQuery():
    gasNeeded = request.args.get('gas_needed')
    address = requestself.args.get('public_address')
    speedNeeded = request.args.get('tx_speed')
    return jsonify({"gas requested": gasNeeded}, {"public address": address}, {"speed requested": speedNeeded})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "page not found"})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
