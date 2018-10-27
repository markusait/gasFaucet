from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'It works!'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "page not found"})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
