$(".add-birds").hide();
var locationSearchButton = $(".favorite-search-location")
var speciesSearchButton = $(".favorite-search-species")

locationSearchButton.on('click', function() {
  const url = birdsByLatLongUrl()
  fetchBirds(url)
})

speciesSearchButton.on('click', function() {
  const url = birdsBySpeciesCodeUrl()
  fetchBirds(url)
})

const getLatitude = () => {
  return $('#latitude')[0].value
}

const getLongitude = () => {
  return $('#longitude')[0].value
}

const birdsByLatLongUrl = () => {
  const lat = getLatitude()
  const long = getLongitude()
  const url = `https://ebird.org/ws2.0/data/obs/geo/recent?lat=${lat}&lng=${long}&dist=10`
  return url
}

const getSpeciesCode = () => {
  return $('#species-code')[0].value
}

const birdsBySpeciesCodeUrl = () => {
  const speciesCode = getSpeciesCode()
  const url = `https://ebird.org/ws2.0/ref/taxonomy/ebird?species=${speciesCode}&fmt=json`
  return url
}

const fetchBirds = (url) => {
  const header = {headers: {'X-eBirdApiToken': 'hv9rjmnpb5vo'}}
  fetch(url, header)
    .then((response) => response.json())
    .then((birds) => {
      birds.sort(function(a, b) {
        if (a.comName < b.comName) {
          return 1;
        } else {
          return -1;
        }
      });
      $("#search-container").css("border-bottom", "1px solid lightgray")
      birds.forEach((bird) => {
        if (bird.comName.includes("sp.")) {
        } else {
          $(".search-results").prepend(`<input type="checkbox" value="${bird.speciesCode}/${bird.comName}/${bird.sciName}" class="bird-info">${bird.comName} (${bird.sciName})</option><br>`)
        }
      })
      $(".add-birds").show();
    })
};

const getCheckedBirds = () => {
  favBirds = []
  $('.bird-info:checked').each(function(birdInfo) {
    favBirds.push(this.value)
  })
  return favBirds
}

const postPayload = (body) => {
  return { type: 'POST',
           url: "/api/v1/favorites",
           data: body
         }
}

const addFavoriteBirds = () => {
  const payload = {}
  payload["birds"] = getCheckedBirds()
  $.ajax(postPayload(payload))
  alert('Added to your favorites!')
}

const emailFavSightings = () => {
  $.ajax({
    type: 'GET',
    url: "/api/v1/favorites/observations"
  })
  alert('A report of your favorite bird observations near you is being processed.')
}

map.on('click', function(e) {
  var features = map.queryRenderedFeatures(e.point);

  if (!features.length) {
    return;
  }

  var feature = features[0];

  var popup = new mapboxgl.Popup({ offset: [0, -15] })
    .setLngLat(feature.geometry.coordinates)
    .setHTML('<h3>' + feature.properties.comName
             + '</h3><p> Scientific Name: ' + feature.properties.sciName
             + '</h3><p> Location: ' + feature.properties.locName
             + '</h3><p> Date & Time(24 hr): ' + feature.properties.obsDt
             + '</h3><p> How Many: ' + feature.properties.howMany
             + '</p>')
    .setLngLat(feature.geometry.coordinates)
    .addTo(map);
});

const getSpeciesCodes = () => {
  return $(".species-code").text().split(" ").join(" ").trim().split(" ")
}

const getBirdSightings = (url, header) => {
  return fetch(url, header)
    .then((response) => response.json())
    .then((favSightings) => favSightings)
}

const createGeoJSONCircle = function(center, radiusInKm) {
  var points = 64;
  var coords = {
    latitude: center[1],
    longitude: center[0]
  };
  var km = radiusInKm;
  var ret = [];
  var distanceX = km / (111.320 * Math.cos(coords.latitude * Math.PI / 180));
  var distanceY = km / 110.574;
  var theta, x, y;
  for(var i = 0; i < points; i++) {
    theta = (i / points) * (2 * Math.PI);
    x = distanceX * Math.cos(theta);
    y = distanceY * Math.sin(theta);
    ret.push([coords.longitude + x, coords.latitude + y]);
  }
  ret.push(ret[0]);

  return {
    "type": "geojson",
    "data": {
      "type": "FeatureCollection",
      "features": [{
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [ret]
        }
      }]
    }
  };
};

const createGeoJSONPoints = (sightings) => {
  return sightings.map(function(birdSightings) {
    return birdSightings.map(function(sighting) {
      return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [sighting.lng, sighting.lat]
        },
        "properties": {
          "comName": sighting.comName,
          "sciName": sighting.sciName,
          "locName": sighting.locName,
          "obsDt": sighting.obsDt,
          "howMany": sighting.howMany
        }
      }
    })
  })
}
