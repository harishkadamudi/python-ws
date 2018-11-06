from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This is required')

	@jwt_required()
	def get(self, name):
		#item = next(filter(lambda x: x['name'] == name, items),None)
		#return {'item': item},200 if items is not None else 404
		item = self.find_by_name(name)
		if item:
			return item
		return {'message': 'Item not found'}, 404


	@classmethod
	def find_by_name(cls, name):
		pass
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items WHERE name = ?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()

		connection.commit()
		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}, 200

	def post(self, name):
		#if next(filter(lambda x: x['name'] == name, items), None) is not None:
		#	return {'message': "Item with {} already exists.".format(name)}, 400

		#data = Item.parser.parse_args()
		#data = request.get_json()
		#item = {'name': name, 'price': data['price']}
		#items.append(item)
		#return items, 201

		if self.find_by_name(name):
			return {'message': "Item with {} already exists.".format(name)}, 400

		data = self.parser.parse_args()
		item = {'name': name, 'price': data['price']}

		try:
			self.insert(item)
		except:
			return {'message': 'An error occured while performing the operation'}, 500

		return item, 201

	@classmethod
	def insert(clsc, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		sql = "INSERT INTO items values (?, ?)"

		cursor.execute(sql, (item['name'], item['price'],))

		connection.commit()
		connection.close()

	def delete(self, name):
		#global items
		#items = list(filter(lambda x: x in x['name'] != name, items))
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		sql = "DELETE FROM items where name =  ?"

		cursor.execute(sql, (name,))

		connection.commit()
		connection.close()

		return {'message': 'item deleted!'}

	def put(self, name):
		data = Item.parser.parse_args()
		#item = next(filter(lambda x: x['name'] == name, items), None)
		item = self.find_by_name(name)
		updatedItem = {'name': name, 'price': data['price']}
		if item is None:
			try:
				self.insert(updatedItem)
			except:
				return {'message': 'error occurred while updating item'}, 500
		else:
			try:
				self.update(updatedItem)
			except:
				return {'message': 'error occurred while updating item'}, 500

		return {'message': 'date updated!', 'data': updatedItem}


	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		sql = "UPDATE items SET price = ? where name =  ?"

		cursor.execute(sql, (item['price'], item['name']))

		connection.commit()
		connection.close()


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		sql = "SELECT * FROM items"
		rows = cursor.execute(sql)
		items = []
		for row in rows:
			items.append({'name': row[0], 'price': row[1]})
		#connection.commit()
		connection.close()
		return {'items': items}

