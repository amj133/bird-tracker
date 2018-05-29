from .ebird_service import EbirdService
from .bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
import ipdb

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/search')
@login_required
def new():
    return render_template('favorites/new.html')

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
            bird = Bird(bird_info[2], bird_info[3], bird_info[1])
            birds.append(bird)

        return render_template('favorites/index.html', birds=birds)

@bp.route('/<int :id>')
@login_required
def show(id):
    db = get_db()
    db.execute(
        'SELECT * FROM bird WHERE bird_id = ?', (id,)
    ).fetchone()
    
