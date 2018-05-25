import pytest
import code
# import unittest
from mock import MagicMock, patch
# from unittest.mock import MagicMock
from flask import g, session
from flaskr.db import get_db
from flaskr.ebird_service import EbirdService

def test_user_dashboard(client, auth):
    res = auth.login()
    response = client.get('/')
    assert client.get('/').status_code == 200
    assert "Tyrannus vociferans" in response.data

    # thing = EbirdService()
    # thing.get_notable_sightings = MagicMock(return_value=3)
    # x = thing.get_notable_sightings()
    # # import ipdb; ipdb.set_trace()
    #
    # assert x == 3
