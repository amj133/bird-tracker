web: gunicorn "birdy:create_app()"
worker: celery worker -A birdy.jobs.background_jobs --loglevel=info
scheduler: celery beat -A birdy.jobs.background_jobs --loglevel=info
