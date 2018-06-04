import sys
sys.path.append('..')
from birdy.services.ebird_service import EbirdService
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from birdy.controllers.auth import login_required
from birdy.db import get_db
from sqlalchemy import text

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    sightings = EbirdService().get_notable_sightings(g.user['latitude'], g.user['longitude'])
    return render_template('dashboard/index.html', sightings=sightings)

@bp.route('/user/edit', methods=('GET', 'POST'))
@login_required
def edit():
    username = g.user['username']
    if request.method == 'GET':
        email = g.user['email']
        return render_template('dashboard/edit.html', username=username, email=email)
    elif request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_preference = request.form['notify']
        query = text('UPDATE birdy_user SET username = :new_username, email = :new_email WHERE username = :old_username')
        query = query.bindparams(new_username=new_username, new_email=new_email, old_username=username)
        get_db().engine.execute(query)

    return redirect(url_for('index'))
