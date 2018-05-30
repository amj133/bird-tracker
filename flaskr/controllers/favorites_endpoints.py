from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('favorites_endpoints', __name__, url_prefix='/api/v1')

@bp.route('/favorites', methods=['POST'])
@login_required
def create():
    bird_info = request.form.getlist('birds[]')
    db = get_db()
    user_id = g.user['id']

    for info in bird_info:
        species_code = info.split("/")[0]
        common_name = info.split("/")[1]
        sci_name = info.split("/")[2]
        db.execute(
            'INSERT INTO bird (species_code, common_name, sci_name) VALUES (?, ?, ?)', (species_code.encode('utf8'), common_name, sci_name)
        )
        bird_id = db.execute(
            'SELECT bird.id FROM bird WHERE species_code = ?', (species_code.encode('utf8'),)
        ).fetchone()
        db.execute(
            'INSERT INTO user_birds (user_id, bird_id) VALUES (?, ?)', (int(user_id), bird_id[0])
        )
        db.commit()

    return "Favorites Added"
