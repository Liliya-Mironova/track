from flask import request, jsonify, url_for
from app import app, oauth, jsonrpc, model
import base64

from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, VK, Google

OAUTH_BACKENDS = [
    Google, VK
]

@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))

def handle_authorize_vk(remote, token, user_info):
    model.autenticate('vk', user_info)
    return jsonify(user_info)

def handle_authorize_google(remote, token, user_info):
    model.autenticate('google', user_info)
    return jsonify(user_info)

for backend in OAUTH_BACKENDS:
    if backend == Google:
        bp = create_flask_blueprint(backend, oauth, handle_authorize_google)
        app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))
    if backend == VK:
        bp = create_flask_blueprint(backend, oauth, handle_authorize_vk)
        app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))


@jsonrpc.method('find_user')
# надо брать токен из сессии и если авторизован, то выполнять
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
    #   arr.append(m['content'])
    # resp = jsonify({'messages': arr})
    resp = jsonify(messages)
    resp.status_code = 200
    return resp


@jsonrpc.method('api.upload_file')
def upload_file (b64content, filename):
    return b64content


# python3 run.py
# https://console.developers.google.com/apis/credentials/oauthclient/376891051682-qovomi5amba9t7tpt477acr55cpfm8go.apps.googleusercontent.com?project=messenger-223008