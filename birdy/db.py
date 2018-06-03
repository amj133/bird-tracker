import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

def get_db():
    if 'db' not in g:
        g.db = current_app.db

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.engine.dispose()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.engine.execute(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
