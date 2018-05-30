from .ebird_service import EbirdService
from .bird import Bird
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
import ipdb

bp = Blueprint('bird_search', __name__, url_prefix='/search')

@bp.route('/species')
@login_required
def by_species():
    return render_template('search/by_species.html')
