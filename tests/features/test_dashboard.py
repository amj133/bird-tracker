import pytest
import ipdb
from flask import g, session
from birdy.db import get_db
from sqlalchemy import text

def test_user_dashboard(client, auth):
    res = auth.login()
    response = client.get('/')
    assert client.get('/').status_code == 200
    assert "Scientific Name:" in response.data
    assert "Observation Date:" in response.data
    assert "Location:" in response.data
    assert "How Many:" in response.data

def test_user_can_edit_profile(client, auth, app):
    res = auth.login()
    with app.app_context():
        query = "SELECT * FROM birdy_user WHERE id = 1"
        billy = get_db().engine.execute(query).fetchone()

        assert 1 == billy[0]
        assert 'daily' == billy[3]
        assert "billy" == billy[4]
        assert 'billy@example.com' == billy[5]

        client.post(
            '/user/edit',
            data={'username': 'billyRocks', 'email': 'billyrocks@example.com', 'notify': 'weekly'}
        )
        query = "SELECT * FROM birdy_user WHERE id = 1"
        updated_billy = get_db().engine.execute(query).fetchone()

        assert 1 == updated_billy[0]
        assert 'weekly' == updated_billy[3]
        assert "billyRocks" == updated_billy[4]
        assert "billyrocks@example.com" == updated_billy[5]
