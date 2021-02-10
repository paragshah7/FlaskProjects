import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books_list = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'language': 'English'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'language': 'Danish'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'language': 'French'}
]


@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            return 'Nothing found', 404
    
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        iD = books_list[-1]['id']+1

        new_obj = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }

        books_list.append(new_obj)
        return jsonify(books_list), 201

# @app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def single_book(id):
#     if request.method == 'GET':
#         for book in books_list:
#             if book['id'] == id:
#                 return jsonify(book)
#             pass
#     if request.method == 'PUT':
#         for book in books_list:
#             if book['id'] == id:


app.run()



"""
Test using Postman
https://www.youtube.com/watch?v=8L_otSDvmR0&list=PLMOobVGrchXN5tKYdyx-d2OwwgxJuqDVH&index=4
"""
