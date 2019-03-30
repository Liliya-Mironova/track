from app import app, mail, celery
from flask_mail import Message
from instance import config

# msg = Message(
#     "Hello",
#     sender="mironova.lr@phystech.edu",
#     recipients=["theflower86@mail.ru"]
# )

# msg

# msg.body = "testing"
# msg.html = "<b>testing</b>"

# with app.app_context():
#     mail.send(msg)

@celery.task(soft_time_limit=3, time_limit=10)
def send_email_ ():
    message = Message('HW', sender=app.config['ADMINS'][0], recipients=[])
    message.html = '<b>testing</b>';

    with app.app_context():
        mail.send(message)