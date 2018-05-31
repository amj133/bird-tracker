import sys
sys.path.append('..')
from birdy.services.ebird_service import EbirdService
from birdy.services.bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from birdy.controllers.auth import login_required
from birdy.db import get_db
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
