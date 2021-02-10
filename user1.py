import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
users_list = [
    {'id': 0,
     'first_name': 'Parag',
     'last_name': 'Shah',
     'username': 'pshah@gmail.com',
     'password': 'Parag123'},
    {'id': 1,
     'first_name': 'Sanika',
     'last_name': 'Nikam',
     'username': 'snikam@gmail.com',
     'password': 'Parag123'},
    {'id': 2,
     'first_name': 'Sandy',
     'last_name': 'Shah',
     'username': 'sshah@gmail.com',
     'password': 'Parag123'},
]


@app.route('/v1/user', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        if len(users_list) > 0:
            return jsonify(users_list)
        else:
            return 'Nothing found', 404

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        iD = users_list[-1]['id']+1

        new_obj = {
            'id': iD,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password
        }

        users_list.append(new_obj)
        return jsonify(users_list), 201
    

# @app.route('/v1/user/self', methods=['GET', 'PUT', 'DELETE'])
# def users():
    

app.run(debug=True)


"""
Test using Postman
https://www.youtube.com/watch?v=8L_otSDvmR0&list=PLMOobVGrchXN5tKYdyx-d2OwwgxJuqDVH&index=4
"""
