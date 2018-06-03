web: gunicorn "birdy:create_app()"
worker: celery worker -A birdy.jobs.background_jobs --loglevel=info
