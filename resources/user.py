from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username can\'t be blank')
    parser.add_argument('password', required=True, type=str, help='Password can\'t be blank')

    def post(self):

        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already Exits!!'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created Successfully"}, 201
