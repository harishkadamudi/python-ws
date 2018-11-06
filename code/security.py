from user import User
from werkzeug.security import safe_str_cmp

user = [
	User(1, 'bod', 'password')
]

username_mapping = {u.username: u for u in user}

userid_mapping = {u.id: u for u in user}


def authenticate(username, password):
	#user = username_mapping.get(username,None)
	user = User.find_by_username(username)

	if user and safe_str_cmp(user.password, password):
		return user


def identity(payload):
	user_id = payload['identity']
	#return userid_mapping.get(user_id,None)
	return User.find_by_id(user_id)