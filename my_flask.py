from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'MyWonderfulstore',
        'items': [
            {
                'name': 'Item1',
                'price': 15.99
            }
        ]
    }
]


# welcome handler
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!!'


# post store request
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    stores.append(request_data)
    return jsonify({'stores': stores})


# get store request GET /
@app.route("/store")
def get_stores():
    return jsonify({'stores': stores})


# get store by name GET /storename
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'No Store Found!!'})


# POST /store/<string:name>/item {name:price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    items = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append(items)
        return jsonify({'stores': stores})
    return jsonify({'message': 'something went wrong'})


# get store by name GET /storename
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'No Items found!!'})


if __name__ == '__main__':
    app.run(port=5000)
