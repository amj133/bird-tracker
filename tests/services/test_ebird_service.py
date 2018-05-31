import pytest
from mock import MagicMock, patch
from flask import g, session
from birdy.db import get_db
from birdy.services.ebird_service import EbirdService

@patch('birdy.services.ebird_service.EbirdService.get_notable_sightings')
def test_instance_methods_get_notable_sightings(self):
    service = EbirdService()
    service.get_notable_sightings.return_value = [
        {
            'comName': 'big bird',
            'sciName': 'birdus largus',
            'obsDt': '2-13-2018',
            'lat': '39.34',
            'lng': '-152.27',
            'howMany': 3,
            'locName': 'Great Lake'
        }
    ]
    response = service.get_notable_sightings()

    assert response != None
    assert type(response) == list
    assert type(response[0]) is dict
    assert response[0]['comName'] == 'big bird'
