from app import db


def list_messages_by_chat(chat_id, limit):
	return db.query_all("""
		SELECT user_id, nick, name,
			   message_id, content, added_at
		FROM messages
		JOIN users USING (user_id)
		WHERE chat_id=%(chat_id)s
		ORDER BY added_at DESC
		LIMIT %(limit)s
	""", chat_id=int(chat_id), limit=int(limit))

def find_user(name):
	return db.query_all("""
		SELECT user_id
		FROM USERS
		WHERE name=%(name)s OR nick=%(name)s
	""", name=name)

def find_chat(name):
	return db.query_all("""
		SELECT topic
		FROM chats
		JOIN members USING (chat_id)
		JOIN users USING (user_id)
		WHERE users.name=%(name)s
	""", name=name)

def create_private_chat(name, othername, topic):
	user_id = find_user(name)
	other_id = find_user(othername)
	print (user_id)
	print (other_id)
	
	db.insert("""
		INSERT INTO chats (is_group_chat, topic) 
		VALUES(false,%(topic)s)
	""", topic=topic)

	chat_id = db.get_cursor().lastrowid
	print (chat_id)

	db.insert("""
		INSERT INTO members (user_id, chat_id) 
		VALUES(%d,%s), (user_id,chat_id)
	""", user_id=int(user_id), chat_id=int(chat_id))

	db.insert("""
		INSERT INTO members (user_id, chat_id) 
		VALUES(%d,%s), (user_id,chat_id)
	""", user_id=int(other_id), chat_id=int(chat_id))