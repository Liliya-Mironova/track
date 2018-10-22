import unittest
from app import app


class AppTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_index(self):
		rv = self.app.get('/')
		self.assertEqual(200, rv.status_code)
		self.assertEqual(b'Hello, world!', rv.data)
		self.assertEqual("text/html", rv.mimetype)
# -----------------------------------------------------
	def test_login(self):
		rv = self.app.post('/login/', data={"first_name":"Jesse","user_nickname":"Pinkman"})
		self.assertEqual(b'{"first_name":"Jesse","user_nickname":"Pinkman"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	# def test_find_user(self):
	# 	rv = self.app.get('/find_user/', data={"full_name":"Jesse","user_nickname":"Jess"})
	# 	self.assertEqual(b'{"full_name":"Jesse","user_nickname":"Jess"}\n', rv.data)
	# 	self.assertEqual(200, rv.status_code)
	# 	self.assertEqual("application/json", rv.mimetype)

	def test_find_chat(self):
		rv = self.app.get('/find_chat/', data={"chat_name":"chat1","chat_nickname":"chat2"})
		self.assertEqual(b'{"chat_name":"chat1","chat_nickname":"chat2"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_get_chats_list(self):
		rv = self.app.get('/get_chats_list/')
		self.assertEqual(b'{"name":"Liliya","nickname":"LL","participant":5}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_create_private_chat(self):
		rv = self.app.get('/create_private_chat/')
		self.assertEqual(b'{"name":"new private_chat"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_create_group_chat(self):
		rv = self.app.get('/create_group_chat/')
		self.assertEqual(b'{"name":"new group_chat"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_add_users_to_chat(self):
		rv = self.app.get('/add_users_to_chat/')
		self.assertEqual(b'{"action":"add user"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_leave_chat(self):
		rv = self.app.get('/leave_chat/')
		self.assertEqual(b'{"action":"leave chat"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_send_message(self):
		rv = self.app.get('/send_message/')
		self.assertEqual(b'{"action":"send message"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_read_message(self):
		rv = self.app.get('/read_message/')
		self.assertEqual(b'{"text":"ok","user":"Liliya"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)

	def test_load_file(self):
		rv = self.app.post('/load_file/')
		self.assertEqual(b'{"action":"new file"}\n', rv.data)
		self.assertEqual(200, rv.status_code)
		self.assertEqual("application/json", rv.mimetype)	

	# def tearDown(self):
	# 	rv = self.app.get('/')
	# 	self.assertEqual(200, rv.status_code)
	# 	self.assertEqual("application/json", rv.mimetype)


if __name__ == "__main__":
  	unittest.main()

# python -m unittest tests/app_tests.py