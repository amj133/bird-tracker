from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('favorites_endpoints', __name__, url_prefix='/api/v1')

@bp.route('/favorites', methods=['POST'])
def create():
    species_code = request.form['species_code']
    user_id = request.form['user_id']
    # if g.user['id'] == user_id
    db = get_db()

    db.execute(
        'INSERT INTO bird (species_code) VALUES (?)', (species_code)
    )

    bird_id = db.execute(
        'SELECT bird.id FROM bird WHERE species_code = ?', (species_code)
    ).fetchone()

    db.execute(
        'INSERT INTO user_birds (user_id, bird_id) VALUES (?, ?)', (user_id, bird_id)
    )

    flash("Successfully added to favorites!")
