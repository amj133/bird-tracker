from celery.schedules import crontab

CELERY_IMPORTS = ('birdy.jobs.background_jobs')
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'send_fav_sightings_emails': {
        'task': 'birdy.jobs.background_jobs.send_nightly_emails',
        'schedule': crontab(),
        'args': ()
    },
}
