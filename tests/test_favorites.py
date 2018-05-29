import pytest
import ipdb
from flask import g, session
from flaskr.db import get_db

def test_user_favorites_none_if_not_added(client, auth):
    res = auth.login()
    response = client.get('/favorites/')

    assert response.status_code == 200
    assert "Go to search to add favorite birds!" in response.data

def test_user_favorites_displayed(client, auth, app):
    res = auth.login()
    with app.app_context():
        get_db().execute("INSERT INTO bird (species_code, common_name, sci_name) VALUES ('bgbrd', 'Big Bird', 'Birdus largus')")
        get_db().execute('INSERT INTO user_birds (user_id, bird_id) VALUES (1, 1)')
        response = client.get('/favorites/')
        assert 'Big Bird' in response.data
        assert 'Birdus largus' in response.data
        assert 'bgbrd' in response.data

def test_user_favorites_search(client, auth):
    res = auth.login()
    response = client.get('/favorites/search')

    assert client.get('/').status_code == 200
    assert "Latitude" in response.data
    assert "Longitude" in response.data
    assert "Search" in response.data
