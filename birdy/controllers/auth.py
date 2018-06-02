import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from birdy.db import get_db
from sqlalchemy import text

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        latitude = str(request.form['latitude'])
        longitude = str(request.form['longitude'])
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.engine.execute(
            text('SELECT id FROM birdy_user WHERE username = :username').bindparams(username=username)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            query = text("INSERT INTO birdy_user (username, password, latitude, longitude) VALUES (:username, :password, :latitude, :longitude)")
            query = query.bindparams(username=username, password=generate_password_hash(password), latitude=latitude, longitude=longitude)
            db.engine.execute(query)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        query = text('SELECT * FROM birdy_user WHERE username = :username')
        query = query.bindparams(username=username)
        user = db.engine.execute(query).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        query = text('SELECT * FROM birdy_user WHERE id = :user_id')
        query = query.bindparams(user_id=user_id)
        g.user = get_db().engine.execute(query).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
