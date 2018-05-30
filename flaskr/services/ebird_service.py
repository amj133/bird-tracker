import requests
from .bird_sighting import BirdSighting

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
                sighting['comName'],
                sighting['sciName'],
                sighting['obsDt'],
                sighting['lat'],
                sighting['lng'],
                sighting['howMany'],
                sighting['locName']
            )
            sightings.append(new_sighting)
        return sightings

    def get_notable_sightings(self, latitude, longitude):
        url = 'https://ebird.org/ws2.0/data/obs/geo/recent/notable'
        header = {'X-eBirdApiToken': 'hv9rjmnpb5vo'}
        params = {'lat': latitude, 'lng': longitude, 'maxResults': '10'}
        json_sightings = self.get_response(url, header, params)
        return self.create_bird_sightings(json_sightings)

    def get_recent_nearby_sightings(self, latitude, longitude):
        url = 'https://ebird.org/ws2.0/data/obs/geo/recent'
        header = {'X-eBirdApiToken': 'hv9rjmnpb5vo'}
        params = {'lat': latitude, 'lng': longitude, 'maxResults': '10', 'dist': '25'}
        json_sightings = self.get_response(url, header, params)
        return self.create_bird_sightings(json_sightings)
