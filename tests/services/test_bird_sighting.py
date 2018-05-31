import pytest
from birdy.services.bird_sighting import BirdSighting

def test_bird_sighting_has_attributes():
    attributes = {
        'comName': 'big bird',
        'sciName': 'birdus largus',
        'obsDt': '2-13-2018',
        'lat': '39.34',
        'lng': '-152.27',
        'howMany': 3,
        'locName': 'Great Lake'
    }

    sighting = BirdSighting(
        attributes['comName'],
        attributes['sciName'],
        attributes['obsDt'],
        attributes['lat'],
        attributes['lng'],
        attributes['howMany'],
        attributes['locName']
    )

    assert type(sighting) == BirdSighting
    assert sighting.com_name == 'big bird'
    assert sighting.sci_name == 'birdus largus'
    assert sighting.obs_date == '2-13-2018'
    assert sighting.latitude == '39.34'
    assert sighting.longitude == '-152.27'
    assert sighting.how_many == 3
    assert sighting.location == 'Great Lake'
