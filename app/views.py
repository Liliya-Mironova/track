from flask import request, jsonify, url_for, redirect, make_response, session
from app import app, oauth, jsonrpc, model, cent_client, s3_client, db, models
from instance import config
import base64
import time
import jwt
import json

# authentication
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, VK, Google

OAUTH_BACKENDS = [
    Google, VK
]

from .models import User, Password, Chat, Message, Attachment

# forms validation (wftorms)
from .wtforms import UserForm
import requests
from werkzeug.datastructures import ImmutableMultiDict

# --------------------------------------------------------------------------------------
# authentication
@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))

def handle_authorize_vk (remote, token, user_info): # works!
    #model.autenticate('vk', user_info)
    site = 'vk'
    session['username'] = user_info['given_name']

    is_registered = User.query.filter(User.external_id == site + ':' + user_info['sub']).all()
    print (is_registered)
    if len(is_registered) == 0:
        users = User(None, user_info['given_name'], user_info['given_name'], site + ':' + user_info['sub'])
        db.session.add(users)
        db.session.commit()

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
def handle_authorize_google (remote, token, user_info): # works!
    #model.autenticate('google', user_info)

    site = 'google'
    session['username'] = user_info['given_name']

    is_registered = User.query.filter(User.external_id == site + ':' + user_info['sub']).all()
    print (is_registered)
    if len(is_registered) == 0:
        users = User(None, user_info['given_name'], user_info['given_name'], site + ':' + user_info['sub'])
        db.session.add(users)
        db.session.commit()

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
@app.route('/create/<string:id>/<string:name>/<string:nick>')
def create_user (id, name, nick): # only demo, works!
    users = User(id, name, nick)
    db.session.add(users)
    db.session.commit()

    resp = jsonify(users.user_id)
    resp.status_code = 200
    return resp

@app.route('/auth1', methods=['GET'])
def auth1 (): # only demo, works!
    #user_id = model.check_user(login)

    print (request.args) # ImmutableMultiDict([('login', 'lmironov'), ('password', '11')])
    form = UserForm(request.args)
    print (form.data) # {'login': 'lmironov', 'password': '11'}
    if form.validate():
        print ('val')
    return "OK"
    #     form.populate_obj(user)
    #     User.query.all()

@jsonrpc.method('auth')
def auth (login, password): # works!
    #user_id = model.check_user(login)

    params = json.loads(request.data)['params'] # sooo hardcode because of jsonrpc
    form = UserForm(ImmutableMultiDict([('login', params[0]), ('password',params[1])]))
    if form.validate():
        user_info = User.query.filter(User.nick == login).all()
        if len(user_info):
            user_id = user_info[0].user_id
        else:
            user_id = None

        if user_id:
            #is_valid = model.check_password(user_id, password)
            is_valid = Password.query.filter(Password.user_id == user_id, Password.password_hash == password).all()

            if len(is_valid):
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
    else:
        resp = jsonify({"Error": "Invalid values"}) # or what?
        resp.status_code = 404 # or what?
    print (resp.data)
    return resp

@jsonrpc.method('find_user')
def find_user (nick): # works!
    # user_names = model.find_user(name)

    users = User.query.filter_by(nick=nick).all()
    arr = []
    for u in users:
        arr.append(u.name)

    resp = jsonify({'users': arr})
    resp.status_code = 200
    return resp

@jsonrpc.method('find_chat')
def find_chat (nick): # works!
    # if session['username'] is not None:
    #     print (session['username'])
    # topics = model.find_chat(name)

    topics = Chat.query.join('members').filter_by(nick=nick).values('topic')
    arr = []
    for t in topics:
        arr.append(t[0])
    resp = jsonify({'chats': arr})

    resp.status_code = 200
    return resp

@jsonrpc.method('create_private_chat')
def create_private_chat (user_id, other_user_id, topic): # works!
    # model.create_private_chat(user_id, other_user_id, topic)

    chat = Chat(is_group_chat=False, topic=topic)

    user1 = User.query.filter(User.user_id == user_id).one()
    user2 = User.query.filter(User.user_id == other_user_id).one()
    chat.members = [user1, user2]

    db.session.add(chat)
    db.session.commit()

# https://github.com/centrifugal/cent
@jsonrpc.method('send_message')
def send_message (user_id, chat_id, content, attach_id): # works!
    # TODO: validate chat_id
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

    # model.send_message(user_id, chat_id, content, attach_id)

    message = Message(chat_id, user_id, content)
    db.session.add(message)
    db.session.query(Chat).filter(Chat.chat_id==chat_id).update({'last_message': content})
    db.session.commit()

    resp = jsonify({'sent': 'yes'})
    resp.status_code = 200
    return resp

@jsonrpc.method('read_message') # ?
def read_message (user_id, chat_id, message_id):
    #model.read_message(user_id, chat_id, message_id)

    last_read_message_id = Chat.query.all()
    print (last_read_message_id[0])
    #db.session.query(Chat).filter(Chat.chat_id==chat_id).update(members: {last_read_message_id: message_id, new_messages: })
    #chat.members = [user1, user2]

    # db.insert("""
    #     UPDATE members
    #     SET last_read_message_id = %(message_id)s
    #     WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    # """, chat_id=int(chat_id), user_id=int(user_id), message_id=int(message_id))

    # db.insert("""
    #     UPDATE members
    #     SET new_messages = new_messages - 1
    #     WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    # """, chat_id=int(chat_id), user_id=int(user_id), message_id=int(message_id))

@jsonrpc.method('list_messages_by_chat')
def list_messages_by_chat (chat_id, limit): # works!
    #messages = model.list_messages_by_chat(chat_id, limit)

    messages = Message.query.filter(Message.chat_id == chat_id).order_by(Message.added_at.desc()).limit(limit).all()
    arr = []
    for m in messages:
        arr.append(m.content)

    resp = jsonify({'messages': arr})
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

# celery = make_selery(app)

# @celery.task()
# def add_together(a, b):
#     return a + b

# @app.route('/news')
# def test ():
#     params = {"channels": ["news"], "data": {"input": "hello"}}
#     cent_client.add("broadcast", params)
#     cent_client.send()
#     return "OK"

# python3 run.py
# https://console.developers.google.com/apis/credentials/oauthclient/376891051682-qovomi5amba9t7tpt477acr55cpfm8go.apps.googleusercontent.com?project=messenger-223008