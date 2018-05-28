from .ebird_service import EbirdService
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    if g.user != None:
        sightings = EbirdService().get_notable_sightings(g.user['latitude'], g.user['longitude'])
        db = get_db()
        return render_template('dashboard/index.html', sightings=sightings)
    else:
        return render_template('dashboard/error.html')
