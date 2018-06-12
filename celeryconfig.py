from celery.schedules import crontab

CELERY_IMPORTS = ('birdy.jobs.background_jobs')
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'send_daily_fav_sightings_emails': {
        'task': 'birdy.jobs.background_jobs.send_daily_sightings_emails',
        'schedule': crontab(hour=6, minute=1),
        'args': ()
    },
    'send_weekly_fav_sightings_emails': {
        'task': 'birdy.jobs.background_jobs.send_weekly_sightings_emails',
        'schedule': crontab(day_of_week=5, hour=12, minute=1),
        'args': ()
    },
    'send_monthly_fav_sightings_emails': {
        'task': 'birdy.jobs.background_jobs.send_monthly_sightings_emails',
        'schedule': crontab(day_of_month='12', hour=6, minute=1),
        'args': ()
    }
}
