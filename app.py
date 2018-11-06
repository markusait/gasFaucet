from sendWeb3Transaction import Web3Transaction
from config import APP_KEY, CACHE_INTERVAL
from flask import Flask, jsonify, request, abort, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
from threading import Timer

app = Flask(__name__)

app.config['SECRET_KEY'] = APP_KEY


#new Tx instance to make sure the prices are kept updated
newTx = Web3Transaction()
#keeping the prices up to date
Timer(CACHE_INTERVAL, newTx.keepCacheWarm).start()



#form for the frontend
class ReusableForm(Form):
     # speed = SelectField('Speed:',choices = [('fast'), ('medium'),('slow')])
     speed = TextField('Speed:', validators=[validators.required(), validators.Length(min=3, max=7)])
     gasNeeded = TextField('GasNeeded:', validators=[validators.required(), validators.Length(min=0, max=30)])
     ethaddress = TextField('Ethaddress:', validators=[validators.required(), validators.Length(min=39, max=43)])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
         speed = request.form['speed']
         ethaddress = request.form['ethaddress']
         gasNeeded = int(request.form['gasNeeded'])
    if form.validate():
         response = newTx.sendTransaction(gasNeeded, speed, ethaddress)
         flash(response)
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
        response = newTx.sendTransaction(gasNeeded, speed, address)
        return jsonify(response)
    # handleing exceptions
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        #return jsonify(sendTransaction(gasNeeded, speed, address))
        raise InvalidUsage(message, status_code=400)


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
