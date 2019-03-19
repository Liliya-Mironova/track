import unittest
import json
from app import app
from jsondiff import diff
from unittest.mock import patch


def mock_find_user(name):
  return {"users": [ {
                              "avatar": None,  
                              "nick": "KirillAkimov",
                              "name": "kakimov",
                              "user_id": 2
                            }, 
                            {
                              "avatar": None, 
                              "name": "alavrentev", 
                              "nick": "KirillLavrentev", 
                              "user_id": 3
                            } ] }

class JSONRPCTest (unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('app.views.find_user', side_effect=mock_find_user)
    def test_find_user(self):
        rpc_query = {"jsonrpc": "2.0", "method": "find_user", "params": ["iri"], "id": 1}
        rpc_expected =   {"users": [ {
                              "avatar": None,  
                              "nick": "KirillAkimov",
                              "name": "kakimov",
                              "user_id": 2
                            }, 
                            {
                              "avatar": None, 
                              "name": "alavrentev", 
                              "nick": "KirillLavrentev", 
                              "user_id": 3
                            } ] }
        rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
        # print(diff(rpc_expected, json.loads(rv.data)))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rpc_expected, json.loads(rv.data))

    def test_find_chat(self):
        rpc_query = {"jsonrpc": "2.0", "method": "find_chat", "params": ["lmironov"], "id": 1}
        rpc_expected = {
                          "chats": [
                            {
                              "chat_id": 1, 
                              "is_group_chat": False, 
                              "last_message": None, 
                              "last_read_message_id": None,
                              "new_messages": 0, 
                              "topic": "dialogkl"
                            }, 
                            {
                              "chat_id": 3, 
                              "is_group_chat": False, 
                              "last_message": "new_message", 
                              "last_read_message_id": None, 
                              "new_messages": 0, 
                              "topic": "dialogld"
                            }
                          ]
                        }
        rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rpc_expected, json.loads(rv.data))

    def test_list_messages_by_chat(self):
        rpc_query = {"jsonrpc": "2.0", "method": "list_messages_by_chat", "params": [1, 2], "id": 1}
        rpc_expected = [{'added_at': 'Sun, 28 Oct 2018 16:39:54 GMT',
                         'chat_id': 1,
                         'content': 'Hello, Lily!',
                         'message_id': 3, 'user_id': 2
                        },
                        {
                         'added_at': 'Sun, 28 Oct 2018 16:39:54 GMT', 
                         'chat_id': 1, 'content': 'Hello, Kirill!',
                         'message_id': 2, 'user_id': 1
                        }]
                
        rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rpc_expected, json.loads(rv.data))

    # def test_create_private_chat(self):
    #     rpc_query = {"jsonrpc": "2.0", "method": "create_private_chat", "params": [1, 2, "mytopic"], "id": 1}
    #     rpc_expected = {
    #                       "id": 1, 
    #                       "jsonrpc": "2.0", 
    #                       "result": None
    #                     }
    #     rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
    #     print(rpc_expected)
    #     print(json.loads(rv.data))
    #     self.assertEqual(rpc_expected, json.loads(rv.data))

    # def test_send_message(self):
    #     rpc_query = {"jsonrpc": "2.0", "method": "send_message", "params": [1, 3, "new_message", 1], "id": 1}
    #     rpc_expected = {
    #                       "id": 1, 
    #                       "jsonrpc": "2.0", 
    #                       "result": None
    #                     }
    #     rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
    #     self.assertEqual(rpc_expected, json.loads(rv.data))

    def test_read_message(self):
        rpc_query = {"jsonrpc": "2.0", "method": "read_message", "params": [4, 3, 29], "id": 1}
        rpc_expected = {
                          "id": 1, 
                          "jsonrpc": "2.0", 
                          "result": None
                        }
        rv = self.app.post('/', data=json.dumps(rpc_query), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rpc_expected, json.loads(rv.data))


if __name__ == "__main__":
    unittest.main()


# HOWTO run the tests:
# python3 run.py
# python -m unittest tests/app_tests.py

# HOWTO collect coverage:
# coverage run -m unittest tests/app_tests.py 
# coverage report -m
# coverage html
# cd htmlcov
# python3 -m http.server

# HOWTO launch a check from cmd:
# curl -i -X POST -H "Content-type: application/json" --data @request.json http://127.0.0.1:5000/
# rv = self.app.post('/api/', data='{ "jsonrpc": "2.0", "method": "print_name", "params": [], "id": 1 }', \
#   content_type='application/json')

# HOWTO launch datagrip:
# sh /home/katze/Downloads/DataGrip-2018.2.4/bin/datagrip.sh

# HOWTO (some postgres commands):
# sudo su - postgres
# pg_dump -s track > 000_schema.sql
# ls back/sql/* | sort | xargs psql track -f

# HOWTO lauch postgres:
# psql --host=localhost --user=lmironov track
# [password: lmironov]




# HOWTO lauch memcache: (the cache will work only after its lauch from cmd)
# sudo service memcached restart

# HOWTO launch centrifuge:
# /home/katze/Downloads/centrifuge/centrifugo --admin --config=/home/katze/Downloads/centrifuge/config.json
# localhost:8000
# password: cde5ef64-9719-423c-99ba-710b1b45f685


# HOWTO launch frontend:
# cd /home/katze/2018-FS-11-Frontend-Mironova/
# npm start

# HOWTO lauch backend:
# python3 /home/katze/back/run.py
# NOW:
#/home/katze/back/run.py runserver


# git pull --rebase
# git diff --cached
# git log -p
#         --stat
# git reset