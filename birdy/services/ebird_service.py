import requests
from .bird_sighting import BirdSighting
from birdy import env_variables

class EbirdService(object):
    def __init__(self):
        pass

    def get_response(self, url, headers, params):
        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def create_bird_sightings(self, json_sightings):
        sightings = []
        for sighting in list(json_sightings):
            new_sighting = BirdSighting(
                sighting.get('comName'),
                sighting.get('sciName'),
                sighting.get('obsDt'),
                sighting.get('lat'),
                sighting.get('lng'),
                sighting.get('howMany') or "Not specified",
                sighting.get('locName'),
                sighting.get('speciesCode')
            )
            sightings.append(new_sighting)
        return sightings

    def get_notable_sightings(self, latitude, longitude):
        url = 'https://ebird.org/ws2.0/data/obs/geo/recent/notable'
        header = {'X-eBirdApiToken': env_variables()['ebird_api_key']}
        params = {'lat': latitude, 'lng': longitude, 'maxResults': '10'}
        json_sightings = self.get_response(url, header, params)
        return self.create_bird_sightings(json_sightings)

    def get_nearby_sightings_by_species(self, latitude, longitude, species_code):
        url = 'https://ebird.org/ws2.0/data/obs/geo/recent/{}'.format(species_code)
        header = {'X-eBirdApiToken': env_variables()['ebird_api_key']}
        params = {'lat': latitude, 'lng': longitude, 'maxResults': '10', 'dist': '20'}
        json_sightings = self.get_response(url, header, params)
        if json_sightings == []:
            return None
        return self.create_bird_sightings(json_sightings)
