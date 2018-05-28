import pytest
from flaskr.bird import Bird

def test_bird_has_attributes():
    attributes = {
        'com_name': 'big bird',
        'sci_name': 'birdus largus',
        'species_code': 'bgbrd'
    }

    bird = Bird(
        attributes['com_name'],
        attributes['sci_name'],
        attributes['species_code'],
    )

    assert type(bird) == Bird
    assert bird.com_name == 'big bird'
    assert bird.sci_name == 'birdus largus'
    assert bird.species_code == 'bgbrd'
