from .ebird_service import EbirdService
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/')
def new():
    if g.user != None:
        return render_template('favorites/new.html')
    else:
        return render_template('dashboard/error.html')
