import sys
sys.path.append('..')
from birdy.services.ebird_service import EbirdService
from birdy.services.bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from birdy.controllers.auth import login_required
from birdy.db import get_db
from sqlalchemy import text

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = g.user['id']
    latitude = g.user['latitude']
    longitude = g.user['longitude']
    birds = get_favorite_birds(user_id)
    if birds == []:
        return render_template('favorites/index.html', birds=None)
    else:
        return render_template('favorites/index.html', birds=birds, lat=float(latitude), lng=float(longitude))

@bp.route('/<int:id>', methods=('GET',))
@login_required
def show(id):
    query = text("SELECT * FROM bird WHERE id = :bird_id")
    query = query.bindparams(bird_id=id)
    bird_info = get_db().engine.execute(query).fetchone()
    bird = Bird(bird_info[0], bird_info[2], bird_info[3], str(bird_info[1]))
    sightings = EbirdService().get_nearby_sightings_by_species(g.user['latitude'], g.user['longitude'], bird.species_code)
    return render_template('favorites/show.html', sightings=sightings, bird=bird)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    user_id = g.user['id']
    query = text("DELETE FROM user_birds WHERE user_id = :user_id AND bird_id = :bird_id")
    query = query.bindparams(user_id=user_id, bird_id=id)
    get_db().engine.execute(query)
    return redirect(url_for('favorites.index'))

def get_favorite_birds(user_id):
    query = text("SELECT bird_id FROM user_birds WHERE user_id = :user_id")
    query = query.bindparams(user_id=user_id)
    bird_ids = get_db().engine.execute(query).fetchall()

    if bird_ids == []:
        return None
    else:
        birds = []
        for bird_id in bird_ids:
            query = text("SELECT * FROM bird WHERE id = :bird_id")
            query = query.bindparams(bird_id=bird_id[0])
            bird_info = get_db().engine.execute(query).fetchone()
            bird = Bird(bird_info[0], bird_info[2], bird_info[3], bird_info[1])
            birds.append(bird)
        return birds
