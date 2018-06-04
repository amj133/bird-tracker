from flask_mail import Mail, Message
from flask import current_app
from birdy import celery
from birdy import create_app
from birdy.db import get_db
from sqlalchemy import text
from birdy.services.mail_generator import MailGenerator
import os

def send_email(email, body):
    mail = Mail(current_app)
    msg = Message(
        'Favorite Birds Report',
        sender='frankyrocksallday@gmail.com',
        recipients=[email]
    )
    msg.body = body
    mail.send(msg)

@celery.task
def send_fav_sightings_email(email, body):
    app = create_app()
    app.app_context().push()
    with app.app_context():
        send_email(email, body)

@celery.task
def send_daily_sightings_emails():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.app_context().push()
    with app.app_context():
        query = text("SELECT id, email, latitude, longitude FROM birdy_user WHERE notify = 'daily'")
        users = get_db().engine.execute(query).fetchall()
        for user in users:
            message = MailGenerator().fav_bird_sightings_message(user[0], user[2], user[3])
            if message == "":
                return "no message to send"
            else:
                send_email(user[1], message)

@celery.task
def send_weekly_sightings_emails():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.app_context().push()
    with app.app_context():
        query = text("SELECT id, email, latitude, longitude FROM birdy_user WHERE notify = 'weekly'")
        users = get_db().engine.execute(query).fetchall()
        for user in users:
            message = MailGenerator().fav_bird_sightings_message(user[0], user[2], user[3])
            if message == "":
                return "no message to send"
            else:
                send_email(user[1], message)

@celery.task
def send_monthly_sightings_emails():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.app_context().push()
    with app.app_context():
        query = text("SELECT id, email, latitude, longitude FROM birdy_user WHERE notify = 'monthly'")
        users = get_db().engine.execute(query).fetchall()
        for user in users:
            message = MailGenerator().fav_bird_sightings_message(user[0], user[2], user[3])
            if message == "":
                return "no message to send"
            else:
                send_email(user[1], message)
