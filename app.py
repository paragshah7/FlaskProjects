from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.before_request
def before():
    print("This is executed BEFORE each request.")


@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)


@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name


@app.route('/person/')
def display_json():
    return jsonify({'name': 'Parag',
                    'address': 'Mumbai'})


@app.route('/numbers/')
def print_list():
    return jsonify(list(range(5)))

# Return custom status code - Seen in console
@app.route('/teapot/')
def teapot():
    return "Would you like some tea?", 418


app.run(debug=True)
