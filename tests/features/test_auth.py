import pytest
import code
from flask import g, session
from birdy.db import get_db
from sqlalchemy import text

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'b', 'latitude': '33.22', 'longitude': '-55.44'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        query = text("SELECT * FROM birdy_user WHERE username = :fake")
        query = query.bindparams(fake='a')
        assert get_db().engine.execute(query).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('billy', 'monkey', b'already registered'),
))

def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'latitude': '11.11', 'longitude': '-22.22'}
    )

    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'billy'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('billy', 'b', b'Incorrect password.'),
))

def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
