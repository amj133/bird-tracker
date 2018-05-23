import code
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    if g.user != None:
        db = get_db()
        return render_template('dashboard/index.html')
    else:
        return render_template('dashboard/error.html')
