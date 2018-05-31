from birdy.controllers.favorites import get_favorite_birds
from .ebird_service import EbirdService

class MailGenerator(object):
    def __init__(self):
        pass

    def get_sightings_for_user(self, user_id, latitude, longitude):
        birds = get_favorite_birds(user_id)
        sightings = []
        for bird in birds:
            new_sightings = EbirdService().get_nearby_sightings_by_species(latitude, longitude, bird.species_code)
            sightings.append(new_sightings)
        sightings = list(filter(None, sightings))
        return sightings

    def fav_bird_sightings_message(self, user_id, latitude, longitude):
        message = ""
        sightings = self.get_sightings_for_user(user_id, latitude, longitude)
        for bird_sightings in sightings:
            for bird_sighting in bird_sightings:
                    message += str(bird_sighting.how_many) + " " + bird_sighting.com_name + " ({})".format(bird_sighting.sci_name) + " observed at " + bird_sighting.location + " ({}, {})".format(str(bird_sighting.latitude), str(bird_sighting.longitude)) + " on " + bird_sighting.obs_date + ".\n"
        return message
