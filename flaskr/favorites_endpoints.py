from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
import ipdb

bp = Blueprint('favorites_endpoints', __name__, url_prefix='/api/v1')

@bp.route('/favorites', methods=['POST'])
@login_required
def create():
    species_codes = request.form.getlist('birds[]')
    # ipdb.set_trace()
    # if g.user['id'] == user_id
    db = get_db()
    user_id = g.user['id']

    for code in species_codes:
        db.execute(
            'INSERT INTO bird (species_code) VALUES (?)', (code.encode('utf8'),)
        )
        bird_id = db.execute(
            'SELECT bird.id FROM bird WHERE species_code = ?', (code.encode('utf8'),)
        ).fetchone()
        db.execute(
            'INSERT INTO user_birds (user_id, bird_id) VALUES (?, ?)', (int(user_id), bird_id[0])
        )
        db.commit()

    return "Favorites Added"
    # flash("Successfully added to favorites!")
