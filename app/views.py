from flask import request, jsonify, url_for, redirect, make_response, session
from app import app, oauth, jsonrpc, model, cent_client
from instance import config
import base64
import time
import jwt

# authentication
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, VK, Google

OAUTH_BACKENDS = [
    Google, VK
]

# --------------------------------------------------------------------------------------
# authentication
@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))

def handle_authorize_vk (remote, token, user_info):
    model.autenticate('vk', user_info)
    session['username'] = user_info['given_name']
    # inf = jsonify({'token': token})
    # response = app.response_class(
    #     response = inf,
    #     mimetype = 'application/json',
    #     status = 200
    # )
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # resp = make_response(redirect("http://localhost:3000", code=302))
    # print (token)
    # resp = jsonify({'token': token})
    # resp.status_code = 200
    # return resp
    # resp.set_cookie('userID', str(user_info['user_id']))
    # resp.set_cookie('token', token)
    # return resp
    return jsonify(token)

# TODO
def handle_authorize_google (remote, token, user_info):
    model.autenticate('google', user_info)
    resp = jsonify({'token': token})
    resp.status_code = 200
    return resp
    # return jsonify(user_info)

for backend in OAUTH_BACKENDS:
    if backend == Google:
        bp = create_flask_blueprint(backend, oauth, handle_authorize_google)
        app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))
    if backend == VK:
        bp = create_flask_blueprint(backend, oauth, handle_authorize_vk)
        app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))

@jsonrpc.method('logout') 
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index')) # or what? doesn't work

# --------------------------------------------------------------------------------------
# bd methods
@jsonrpc.method('auth')
# надо брать токен из сессии и если авторизован, то выполнять
def auth (login, password):
    user_id = model.check_user(login)
    if user_id:
        is_valid = model.check_password(user_id, password)
        if is_valid:
            session['username'] = login
            print (session['username'])
            token = jwt.encode({"sub": "0"}, config.VK_CLIENT_SECRET, algorithm='HS256').decode()
            resp = jsonify({"token": token})
            resp.status_code = 200
        else:
            resp = jsonify({"Error": "Invalid password"}) # or what?
            resp.status_code = 404 # or what?
    else:
        resp = jsonify({"Error": "Unregistered"}) # or what?
        resp.status_code = 404 # or what?
    return resp

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
    print ('find_chat')
    topics = model.find_chat(name)
    # if session['username'] is not None:
    #     print (session['username'])
    # topics = model.find_chat(session['username'])
    arr = []
    for t in topics:
        arr.append(t)
    resp = jsonify({'chats': arr})
    resp.status_code = 200
    return resp

@jsonrpc.method('create_private_chat')
def create_private_chat (user_id, other_user_id, topic):
    model.create_private_chat(user_id, other_user_id, topic)

# https://github.com/centrifugal/cent
@jsonrpc.method('send_message')
def send_message (user_id, chat_id, content, attach_id):
    params = {
        "channels": [str(chat_id)],
        "data": {
            'user_id': user_id,
            'content': content,
            'time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    cent_client.add("broadcast", params)
    cent_client.send()

    model.send_message(user_id, chat_id, content, attach_id)
    return "OK" # what to return???

@jsonrpc.method('read_message')
def read_message (user_id, chat_id, message_id):
    # а как читать сообщения из центрифуги?
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

# --------------------------------------------------------------------------------------
# centrifuge
@jsonrpc.method('get_centrifuge_token')
def get_centrifuge_token (user_id):
    return jwt.encode({"sub": "0"}, config.CENTRIFUGO_SECRET).decode()

# --------------------------------------------------------------------------------------
# files
@jsonrpc.method('api.upload_file')
def upload_file (b64content, filename):
    return b64content

# @app.route('/news')
# def test ():
#     params = {"channels": ["news"], "data": {"input": "hello"}}
#     cent_client.add("broadcast", params)
#     cent_client.send()
#     return "OK"

# python3 run.py
# https://console.developers.google.com/apis/credentials/oauthclient/376891051682-qovomi5amba9t7tpt477acr55cpfm8go.apps.googleusercontent.com?project=messenger-223008