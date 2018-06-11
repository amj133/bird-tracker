# bird-tracker
Bird tracker is an application I built during module 4 at Turing using Flask, a lightweight python framework.  It allows users to search for birds based on location or by specific species, and track sightings of these birds relative to their given geographic location.  Users are sent an email report containing nearby sightings of their favorite birds and can choose from daily, weekly, monthly, or no notifications.  Users can also view a map display of their recent favorite bird sightings while logged in to the site.  The email notifications are achieved using scheduled background tasks.  This was implemented using Celery, Celerby Beat, and the crontab along with Redis as the in-memory data store.  

## Reflections
This was the second project I have built using python and I enjoyed the challenge of continuing to learn something new while trying to build a practical application.  There are a lot of similarities in syntax to ruby, which makes for a relatively easy transition.  I struggled most with configuring the lightweight framework and switching from the built in sqlite to a postgresql database.  In terms of configuration, I had difficulty initially setting up my schedule background tasks.  Given that they are operating in a separate dyno on Heroku, they have to still operate within the context of my particular instance of the flask application, requiring me to call the create_app method of my application factory and run the background task within the application context.  This is a good example of a small difference in configuration that would come built into rails active jobs.  In transitioning from sqlite to postgresql, I wanted to build out the application without using an ORM, as I have done in node.js and express; mainly to be able to speak to the merits of either approach.  It proved a little difficult at first to use sqlalchemy in python without an ORM, although I quickly adjusted and enjoyed the freedom of making custom sql queries.  

Moving forward I would like to implement the python Geocoder library so users do not have to enter a specific latitude and longitude upon registration.  I would also like to track bird sightings within a given user's geographic radius, allowing them to see the frequency at which a particular species is observed in their area and what time of the year is best to observe them.  

See the deployed project here: [BirdTracker](https://polar-cliffs-63489.herokuapp.com/auth/login)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

1. clone down this project and change into the directory
```
git clone https://github.com/amj133/bird-tracker
pip install -r requirements.txt
```
2. create and migrate the database
```
flask init-db
```
3. Run flask server and visit http://127.0.0.1:5000 in your browser
```
flask run
```
*visit http://127.0.0.1:5000 in your browser
*enjoy!

## Running the tests

To run the tests, follow the instructions in [Getting Started](#getting-started) above first.  Open the project directory then run pythom -m pytest tests.
```
python -m pytest tests
```

##### Noted libraries used in the application:
* [pytest](https://github.com/pytest-dev/pytest)
* [celery](https://github.com/celery/celery)
* [psycopg2](https://github.com/psycopg/psycopg2)
* [redis-py](https://github.com/andymccurdy/redis-py)
* [mapbox-gl-js](https://www.mapbox.com/mapbox-gl-js/api/)


## Contributing

Feel free to make pull requests or comments to contribute to this application. I am happy to receive your feedback!

## Authors

* [Andrew Jeffery](https://github.com/amj133)

## Acknowledgments

* Thank you to our awesome instructors at Turing for help and guidance during this project!
