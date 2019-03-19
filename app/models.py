from app import db
from datetime import datetime


members = db.Table('members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.chat_id'), primary_key=True),
    db.Column('new_messages', db.String),
    db.Column('last_read_message_id', db.Integer, db.ForeignKey('messages.message_id'))
)

class User (db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    nick = db.Column(db.String(80), unique=True, nullable=False)
    avatar = db.Column(db.String(80))
    external_id = db.Column(db.Integer)

    attachments = db.relationship('Attachment', backref='user', lazy='dynamic',
        primaryjoin="User.user_id==Attachment.user_id")
    passwords = db.relationship('Password', uselist=False, backref='user',
        primaryjoin="User.user_id==Password.user_id")

    members = db.relationship('Chat', secondary=members, lazy='subquery',
                backref=db.backref('pages', lazy=True))

    def __init__(self, name, nick, user_id):
        self.name = name
        self.nick = nick
        if user_id is not None:
            self.user_id = user_id

class Password (db.Model):
    __tablename__ = 'passwords'
    password_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    password_hash = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id, password_hash):
        self.user_id = user_id
        self.password_hash = password_hash

class Chat (db.Model):
    __tablename__ = 'chats'
    chat_id = db.Column(db.Integer, primary_key=True)
    is_group_chat = db.Column(db.Boolean)
    topic = db.Column(db.String(80), nullable=False)
    last_message = db.Column(db.String(80))

    messages = db.relationship('Message', backref='chat')
    attachments = db.relationship('Attachment', backref='chat')

    def __init__(self, is_group_chat, topic):
        self.is_group_chat = is_group_chat
        self.topic = topic

class Message (db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content = db.Column(db.String(80), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    attachments = db.relationship('Attachment', backref='message')
    # members = db.relationship('members', backref='message') # ???

    def __init__(self, chat_id, user_id, content):
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content
        self.added_at = datetime.now()

class Attachment (db.Model):
    __tablename__ = 'attachments'
    attach_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.message_id'))
    type_ = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80))

    def __init__(self, chat_id, user_id, message_id, type_, url=None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.message_id = message_id
        self.type_ = type_
        self.url = url