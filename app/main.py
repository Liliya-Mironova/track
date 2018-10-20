import json
import datetime
import pprint

def application(env, start_resp):
    start_resp('200 OK',  [('Content-Type', 'application/json')])

    current_time = datetime.datetime.now().strftime("%I:%M:%S")
    data = {"time": current_time, "url": env.get('HTTP_HOST', '') + env.get('RAW_URI', '')}

    pprint.pprint(env)

    return [json.dumps(data).encode('utf-8')]
