from flask import Flask, jsonify, request, abort, render_template
from sendWeb3Transaction import sendTransaction
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app = Flask(__name__)


class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])




@app.route('/', methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name=request.form['name']
        print(name)
        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('Error: All the form fields are required. ')
    return render_template('home.html', form=form)



# handeling parameters
@app.route('/fill-wallet-for-gas', methods=['GET'])
def returnQuery():
    # print(request.query_string)
    # args = request.args.to_dict()
    # handeling invalid request parameter
    if not request.args.get('gas_needed'):
        raise InvalidUsage('gas_needed property incorrect', status_code=400)
    if not request.args.get('public_address'):
        raise InvalidUsage(
            'public_address  property incorrect', status_code=400)
    if not request.args.get('tx_speed'):
        raise InvalidUsage('tx_speed property incorrect', status_code=400)
    try:
        gasNeeded = int(request.args.get('gas_needed'))
        address = request.args.get('public_address')
        speed = request.args.get('tx_speed')
        response = sendTransaction(gasNeeded, speed, address)
        print('came all the way here')
        return jsonify(response)
    # handleing exceptions
    except Exception:
        #return jsonify(sendTransaction(gasNeeded, speed, address))
        raise InvalidUsage('Invalid input sent', status_code=400)


#handeling invalid routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "page not found"})

#handeling internal server errors
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "internal server error"})

#custom Error Code
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
