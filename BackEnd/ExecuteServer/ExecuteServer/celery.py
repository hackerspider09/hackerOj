# from __future__ import absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab,timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExecuteServer.settings')

app = Celery("ExecuteServer")
app.conf.enable_utc = False

app.conf.update(timezone = "Asia/Kolkata")
# read config from Django settings, the CELERY namespace would make celery 
# config keys has `CELERY` prefix
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind = True)
def debug_task(self):
   print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'run_pending_submission': {
        'task': 'core.tasks.run_submissions_scheduler',
        'schedule': crontab(minute='*/1'),
    },
    'delete-containers-beats': {
        'task': 'core.tasks.delete_container',
        # change time to delete spawned container to delete if necessory
        'schedule': timedelta(seconds=10),
    },
}


