import pytest
import ipdb
from flaskr.db import get_db

def test_user_favorites_none_if_not_added(client, auth):
    res = auth.login()
    response = client.get('/favorites/')

    assert response.status_code == 200
    assert "Go to search to add favorite birds!" in response.data

def test_user_favorites_displayed(client, auth):
    res = auth.login()
    ipdb.set_trace()
    response = client.get('/favorites/')

    assert response.status_code == 200
    assert "Go to search to add favorite birds!" in response.data

def test_user_favorites_search(client, auth):
    res = auth.login()
    response = client.get('/favorites/search')

    assert client.get('/').status_code == 200
    assert "Latitude" in response.data
    assert "Longitude" in response.data
    assert "Search" in response.data
