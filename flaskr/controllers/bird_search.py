import sys
sys.path.append('..')
from flaskr.services.ebird_service import EbirdService
from flaskr.services.bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.controllers.auth import login_required
from flaskr.db import get_db
import ipdb

bp = Blueprint('bird_search', __name__, url_prefix='/search')

@bp.route('/species')
@login_required
def by_species():
    return render_template('search/by_species.html')

@bp.route('/location')
@login_required
def by_location():
    return render_template('search/by_location.html')
