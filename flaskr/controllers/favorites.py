from .ebird_service import EbirdService
from .bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
import ipdb

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = g.user['id']
    bird_ids = db.execute(
        'SELECT bird_id FROM user_birds WHERE user_id = (?)', (user_id,)
    ).fetchall()

    if bird_ids == []:
        return render_template('favorites/index.html', birds=None)
    else:
        birds = []
        for bird_id in bird_ids:
            bird_info = db.execute(
                'SELECT * FROM bird WHERE id = (?)', (bird_id[0],)
            ).fetchone()
            bird = Bird(bird_info[0], bird_info[2], bird_info[3], bird_info[1])
            birds.append(bird)

        return render_template('favorites/index.html', birds=birds)

@bp.route('/<int:id>', methods=('GET',))
@login_required
def show(id):
    db = get_db()
    bird_info = db.execute('SELECT * FROM bird WHERE id = ?', (id,)).fetchone()
    bird = Bird(bird_info[0], bird_info[2], bird_info[3], bird_info[1])
    sightings = EbirdService().get_recent_nearby_sightings(g.user['latitude'], g.user['longitude'])

    return render_template('favorites/show.html', sightings=sightings, bird=bird)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    user_id = g.user['id']
    db = get_db()
    db.execute(
        'DELETE FROM user_birds WHERE user_id = ? AND bird_id = ?', (user_id, id)
    )
    db.commit()
    return redirect(url_for('favorites.index'))
