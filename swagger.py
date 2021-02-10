import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api, Resource, reqparse
from flask import Flask

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('name', help='Specify your name')


@api.route('/hello/')
class HelloWorld(Resource):
    @api.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        name = args['name']
        return "Hello " + name


if __name__ == '__main__':
    app.run(debug=True)
