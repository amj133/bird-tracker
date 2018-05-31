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
  header = {headers: {'X-eBirdApiToken': 'hv9rjmnpb5vo'}}
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
