import sqlite3
from flask_restful import Resource, Api, request, reqparse


class User:

	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM  users where username = ?"
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM  users where id = ?"
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user


class UserRegistration(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username', required=True, type=str, help='Username can\'t be blank')
	parser.add_argument('password', required=True, type=str, help='Password can\'t be blank')

	def post(self):

		data = UserRegistration.parser.parse_args()

		if User.find_by_username(data['username']):
			return {'message': 'User already Exits!!'},400

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		create_user_sql = "INSERT INTO users VALUES(NULL, ? , ?)"
		cursor.execute(create_user_sql, (data['username'], data['password'],))

		connection.commit()
		connection.close()

		return {"message": "User created Successfully"}, 201