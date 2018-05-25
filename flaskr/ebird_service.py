import requests
import code
from .bird_sighting import BirdSighting

class EbirdService(object):
    def __init__(self):
        pass

    def get_notable_sightings(self, latitude, longitude):
        url = 'https://ebird.org/ws2.0/data/obs/geo/recent/notable'
        header = {'X-eBirdApiToken': 'hv9rjmnpb5vo'}
        payload = {'lat': latitude, 'lng': longitude, 'maxResults': '10'}
        res = requests.get(url, headers=header, params=payload)
        sightings = []

        for sighting in list(res.json()):
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
