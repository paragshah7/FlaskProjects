from flask import Flask
from flask import request, jsonify

app = Flask("my app")
app.config["DEBUG"] = True

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


@app.route('/auth')
def authRouteHandler():

    user = request.authorization["username"]
    passw = request.authorization["password"]

    print(user)
    print(passw)

    auth_display = {user:passw}

    return jsonify(auth_display), 200


@app.route('/v1/user', methods=['GET', 'POST'])
def users():

    if request.method == 'GET':
        return "Please send a POST request for this resource"

    if request.method == 'POST':
        # first_name = request.form['first_name']
        # last_name = request.form['last_name']
        # username = request.form['username']
        # password = request.form['password']
        # iD = users_list[-1]['id']+1

        # new_obj = {
        #     'id': iD,
        #     'first_name': first_name,
        #     'last_name': last_name,
        #     'username': username,
        #     'password': password
        # }

        # users_list.append(new_obj)
        print(request.data)
        print(request.data)
        return request.data, 201




app.run(debug=True)
