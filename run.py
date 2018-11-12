from app import app

if __name__ == "__main__":
	app.run()

	flask.got_request_exception.connect(_rollback_db, app)
	flask.got_request_exception.connect(_commit_db, app)

# python3 run.py