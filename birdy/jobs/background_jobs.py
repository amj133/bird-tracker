from flask_mail import Mail, Message
from flask import current_app
from birdy import celery
from birdy import create_app

@celery.task
def send_email(body):
    app = create_app()
    app.app_context().push()
    with app.app_context():
        mail = Mail(current_app)
        msg = Message(
            'Favorite Birds Report',
            sender='frankyrocksallday@gmail.com',
            recipients=['amj@vt.edu']
        )
        msg.body = body
        mail.send(msg)
