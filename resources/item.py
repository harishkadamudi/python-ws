from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This is required')
	parser.add_argument('store_id', type=int, required=True, help='Store Id can\'t be Blank')

	@jwt_required()
	def get(self, name,store_id):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "Item with {} already exists.".format(name)}, 400

		data = self.parser.parse_args()
		#item = ItemModel(name, data['price'], data['store_id'])
		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			return {'message': 'An error occured while performing the operation'}, 500
		return item.json(), 201

	def delete(self, name):
		item = Item.find_by_name(name)
		if item:
			item.delete_from_db()
		return {"message": 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		if item is None:
			#item = ItemModel(name, data['price'], data['store_id'])
			item = ItemModel(name, **data)
		else:
			item.price = data['price']
			item.store_id = data['store_id']
			
		item.save_to_db()
		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
		#return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}




