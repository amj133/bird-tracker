from .ebird_service import EbirdService
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    sightings = EbirdService().get_notable_sightings(g.user['latitude'], g.user['longitude'])
    return render_template('dashboard/index.html', sightings=sightings)
