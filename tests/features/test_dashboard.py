import pytest
import ipdb
from birdy.db import get_db

def test_user_dashboard(client, auth):
    res = auth.login()
    response = client.get('/')
    assert client.get('/').status_code == 200
    assert "Scientific Name:" in response.data
    assert "Observation Date:" in response.data
    assert "Location:" in response.data
    assert "How Many:" in response.data
