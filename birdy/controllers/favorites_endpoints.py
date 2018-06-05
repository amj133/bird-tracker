from birdy.services.ebird_service import EbirdService
from .favorites import get_favorite_birds
from flask import (
    Blueprint, flash, g, current_app, redirect, render_template, request, url_for
)
from birdy.controllers.auth import login_required
from birdy.db import get_db
from birdy.services.mail_generator import MailGenerator
from sqlalchemy import text
from birdy.jobs.background_jobs import send_fav_sightings_email

bp = Blueprint('favorites_endpoints', __name__, url_prefix='/api/v1')


@bp.route('/favorites', methods=['POST'])
@login_required
def create():
    bird_info = request.form.getlist('birds[]')
    user_id = g.user['id']

    for info in bird_info:
        species_code = str(info.split("/")[0])
        common_name = info.split("/")[1]
        sci_name = info.split("/")[2]

        query = text("SELECT * FROM bird WHERE species_code = :species_code")
        query = query.bindparams(species_code=species_code)

        if get_db().engine.execute(query).fetchone() == None:
            query = text("INSERT INTO bird (species_code, common_name, sci_name) VALUES (:species_code, :common_name, :sci_name)")
            query = query.bindparams(species_code=species_code, common_name=common_name, sci_name=sci_name)
            get_db().engine.execute(query)

        query = text("SELECT bird.id FROM bird WHERE species_code = :species_code")
        query = query.bindparams(species_code=species_code)
        bird_id = get_db().engine.execute(query).fetchone()

        query = text("INSERT INTO user_birds (user_id, bird_id) SELECT :user_id, :bird_id WHERE NOT EXISTS (SELECT * FROM user_birds WHERE user_id = :user_id AND bird_id = :bird_id)")
        # INSERT INTO user_birds (user_id, bird_id)
        #   SELECT 3, 7 WHERE NOT EXISTS
        #   (SELECT * FROM user_birds WHERE user_id = 3 AND bird_id = 7);
        query = query.bindparams(user_id=int(user_id), bird_id=bird_id[0])
        get_db().engine.execute(query)

    # return "Favorites Added"


@bp.route('/favorites/observations', methods=['GET'])
@login_required
def email_fav_sightings():
    user_id = g.user['id']
    email = g.user['email']
    latitude = g.user['latitude']
    longitude = g.user['longitude']
    body = MailGenerator().fav_bird_sightings_message(user_id, latitude, longitude)
    if body == '':
        body = "No recent observations of this species near your location."
    send_fav_sightings_email.delay(email, body)
    return "Sent"
