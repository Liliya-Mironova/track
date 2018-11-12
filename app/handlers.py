from flask import request, jsonify
from app import app, jsonrpc
from app import model

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    callback = url_for(
        'websa_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return remote.authorize_redirect(callback=callback)

@app.route('/login/authorized')
def websa_authorized():
    resp = remote.authorize_access_token()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = remote.get('/user/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@jsonrpc.method('find_user')
def find_user (name):
	user_names = model.find_user(name)
	arr = []
	for u in user_names:
		arr.append(u)
	resp = jsonify({'users': arr})
	resp.status_code = 200
	return resp

@jsonrpc.method('find_chat')
def find_chat (name):
	topics = model.find_chat(name)
	arr = []
	for t in topics:
		arr.append(t)
	resp = jsonify({'chats': arr})
	resp.status_code = 200
	return resp

@jsonrpc.method('create_private_chat')
def create_private_chat (user_id, other_user_id, topic):
	model.create_private_chat(user_id, other_user_id, topic)

@jsonrpc.method('send_message')
def send_message (user_id, chat_id, content, attach_id):
	model.send_message(user_id, chat_id, content, attach_id)

@jsonrpc.method('read_message')
def read_message (user_id, chat_id, message_id):
	model.read_message(user_id, chat_id, message_id)

@jsonrpc.method('list_messages_by_chat')
def list_messages_by_chat (chat_id, limit):
	messages = model.list_messages_by_chat(chat_id, limit)
	# arr = []
	# for m in messages:
	# 	arr.append(m['content'])
	# resp = jsonify({'messages': arr})
	resp = jsonify(messages)
	resp.status_code = 200
	return resp


# python3 run.py