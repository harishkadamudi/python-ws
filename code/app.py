from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from item import Item, ItemList
from user import UserRegistration

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegistration, '/register')


if __name__ == '__main__':
	app.run(port=5000, debug=True)
