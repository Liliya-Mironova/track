from app import db


def autenticate (site, user_info):
    is_registered = db.query_one("""
        SELECT user_id
        FROM USERS
        WHERE external_id = %(external_id)s
    """, external_id=site + ':' + user_info['sub'])

    if not is_registered:
        db.insert("""
            INSERT INTO users (name, external_id) 
            VALUES(%(name)s,%(external_id)s)
        """, name=user_info['given_name'], external_id=site + ':' + user_info['sub']) 

def find_user (name):
    return db.query_all("""
        SELECT user_id, nick, name, avatar
        FROM USERS
        WHERE name LIKE %(regex)s OR nick LIKE %(regex)s
    """, regex='%' + name + '%')

def find_chat (name):
    return db.query_all("""
        SELECT chat_id, is_group_chat, topic, last_message, new_messages, last_read_message_id
        FROM chats
        JOIN members USING (chat_id)
        JOIN users USING (user_id)
        WHERE users.name=%(name)s
    """, name=name)

def list_messages_by_chat (chat_id, limit):
    return db.query_all("""
        SELECT message_id, chat_id, user_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id=%(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
    """, chat_id=int(chat_id), limit=int(limit))

def create_private_chat (user_id, other_user_id, topic):
    db.insert("""
        INSERT INTO chats (is_group_chat, topic) 
        VALUES(false,%(topic)s)
    """, topic=topic)

    chat_id = db.query_one("""
        SELECT MAX(chat_id) 
        FROM chats
    """)
    print (chat_id)

    db.insert("""
        INSERT INTO members (user_id, chat_id) 
        VALUES(%(user_id)s,%(chat_id)s))
    """, user_id=int(user_id), chat_id=int(chat_id))

    db.insert("""
        INSERT INTO members (user_id, chat_id) 
        VALUES(%(user_id)s,%(chat_id)s))
    """, user_id=int(other_user_id), chat_id=int(chat_id))

def send_message (user_id, chat_id, content, attach_id):
    db.insert("""
        INSERT INTO messages (chat_id, user_id, content) 
        VALUES(%(chat_id)s,%(user_id)s,%(content)s)
    """, chat_id=int(chat_id), user_id=int(user_id), content=content)

    # chat_id = db.get_cursor().lastrowid

    db.insert("""
        UPDATE chats 
        SET last_message = %(mes)s 
        WHERE chat_id = %(chat_id)s
    """, mes=content, chat_id=int(chat_id))

    db.insert("""
        UPDATE members 
        SET new_messages = new_messages + 1
        WHERE chat_id = %(chat_id)s AND user_id != %(user_id)s
    """, chat_id=int(chat_id), user_id=int(user_id))

def read_message (user_id, chat_id, message_id):
    db.insert("""
        UPDATE members
        SET last_read_message_id = %(message_id)s
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    """, chat_id=int(chat_id), user_id=int(user_id), message_id=int(message_id))

    db.insert("""
        UPDATE members
        SET new_messages = new_messages - 1
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
    """, chat_id=int(chat_id), user_id=int(user_id), message_id=int(message_id))