from flask import request, jsonify
from app import app
from app import model


@app.route('/messages/')
def messages():
	chat_id = int(request.args.get('chat_id'))
	limit = int(request.args.get('limit'))
	messages = model.list_messages_by_chat(chat_id, limit)
	return jsonify(messages)

# TODO: invalid user
@app.route('/find_user/', methods=['GET']) # http://127.0.0.1:5000/find_user/?name=lmironov
def find_user():
	name = request.args.get('name')
	user_id = model.find_user(name=name)
	resp = jsonify(user_id)
	resp.status_code = 200
	return resp

@app.route('/find_chat/', methods=['GET'])
def find_chat():
	name = request.args.get('name')
	topic = model.find_chat(name=name)
	resp = jsonify(topic)
	resp.status_code = 200
	return resp

@app.route('/create_private_chat/', methods=['GET'])
def create_private_chat():
	name = request.args.get('name')
	# othername = request.args.get('othername')
	# topic = request.args.get('topic')
	othername = 'dpetrov'
	topic = 'dialogdl'
	model.create_private_chat(name=name, othername=othername, topic=topic)