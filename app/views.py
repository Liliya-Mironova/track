from app import app
from flask import request, abort, jsonify


@app.route('/')
def index(name="world"):
	return "Hello, {}!".format(name)

# ----------------------------------------
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return """<html><head></head><body>
        <form method="POST" action="/login/">
            <input name="full_name">
            <input name="user_nickname">
            <input type="submit">
        </form>
        </body></html>"""
    else:
        resp = jsonify(request.form)
        resp.status_code = 200
        return resp

@app.route('/find_user/', methods=['GET', 'POST'])
def find_user():
    if request.method == "POST":
        return """<html><head></head><body>
        <form method="POST" action="/find_user/">
            <input name="full_name">
            <input name="user_nickname">
            <input type="submit">
        </form>
        </body></html>"""   
    else:
        resp = jsonify(request.form)
        resp.status_code = 200
        return resp

@app.route('/find_chat/', methods=['GET', 'POST'])
def find_chat():
    if request.method == "POST":
        return """<html><head></head><body>
        <form method="POST" action="/find_chat/">
            <input name="chat_name">
            <input name="chat_nickname">
            <input type="submit">
        </form>
        </body></html>"""   
    else:
        resp = jsonify(request.form)
        resp.status_code = 200
        return resp

@app.route('/get_chats_list/', methods=['GET'])
def get_chats_list():
    data = {
        'name': 'Liliya',
        'nickname': 'LL',
        'participant': 5
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/create_private_chat/', methods=['GET'])
def create_private_chat():
    data = {'name':'new private_chat'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/create_group_chat/', methods=['GET'])
def create_group_chat():
    data = {'name': 'new group_chat'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/add_users_to_chat/', methods=['GET'])
def add_users_to_chat():
    data = {'action':'add user'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/leave_chat/', methods=['GET'])
def leave_chat():
    data = {'action': 'leave chat'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/send_message/', methods=['GET'])
def send_message():
    data = {'action': 'send message'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/read_message/', methods=['GET'])
def read_message():
    data = {"user": "Liliya", "text": "ok"}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/load_file/', methods=['POST'])
def load_file():
    data = {"action": "new file"}
    resp = jsonify(data)
    resp.status_code = 200
    return resp