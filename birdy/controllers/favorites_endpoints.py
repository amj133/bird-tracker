from birdy.services.ebird_service import EbirdService
from .favorites import get_favorite_birds
from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from birdy.controllers.auth import login_required
from birdy.db import get_db
from flask_mail import Mail, Message
from birdy.services.mail_generator import MailGenerator
from sqlalchemy import text

bp = Blueprint('favorites_endpoints', __name__, url_prefix='/api/v1')


@bp.route('/favorites', methods=['POST'])
@login_required
def create():
    bird_info = request.form.getlist('birds[]')
    # db = get_db()
    user_id = g.user['id']

    for info in bird_info:
        species_code = info.split("/")[0].encode('utf8')
        common_name = info.split("/")[1]
        sci_name = info.split("/")[2]
        query = text("INSERT INTO bird (species_code, common_name, sci_name) VALUES (:species_code, :common_name, :sci_name)")
        query = query.bindparams(species_code=species_code, common_name=common_name, sci_name=sci_name)
        get_db().engine.execute(query)
        query = text("SELECT bird.id FROM bird WHERE species_code = :species_code")
        query = query.bindparams(species_code=species_code)
        bird_id = get_db().engine.execute(query).fetchone()
        # import ipdb; ipdb.set_trace()
        query = text("INSERT INTO user_birds (user_id, bird_id) VALUES (:user_id, :bird_id)")
        query = query.bindparams(user_id=int(user_id), bird_id=bird_id[0])
        get_db().engine.execute(query)
        # db.execute(
        #     'INSERT INTO bird (species_code, common_name, sci_name) VALUES (?, ?, ?)', (species_code.encode('utf8'), common_name, sci_name)
        # )
        # bird_id = db.execute(
        #     'SELECT bird.id FROM bird WHERE species_code = ?', (species_code.encode('utf8'),)
        # ).fetchone()
        # db.execute(
        #     'INSERT INTO user_birds (user_id, bird_id) VALUES (?, ?)', (int(user_id), bird_id[0])
        # )
        # db.commit()

    return "Favorites Added"


@bp.route('/favorites/observations', methods=['GET'])
@login_required
def email_fav_sightings():
    user_id = g.user['id']
    latitude = g.user['latitude']
    longitude = g.user['longitude']
    message = MailGenerator().fav_bird_sightings_message(user_id, latitude, longitude)
    mail = Mail(current_app)
    msg = Message(
        'Favorite Birds Report',
        sender='frankyrocksallday@gmail.com',
        recipients=['amj@vt.edu']
    )
    msg.body = message
    mail.send(msg)
    return "Sent"
