# from __future__ import absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab,timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NCC.settings')

app = Celery("NCC")
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
    'delete-containers-every-30-minutes': {
        'task': 'submission.tasks.run_submissions_scheduler',
        'schedule': crontab(minute='*/1'),
    },
    'delete-containers-beats': {
        'task': 'submission.tasks.delete_container',
        # change time to delete spawned container to delete if necessory
        'schedule': timedelta(seconds=10),
    },
}


#************************************8

# from __future__ import absolute_import , unicode_literals
# import os
# from celery import Celery
# from django.conf import settings
# from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NCC.settings')

# app = Celery("NCC")
# app.conf.enable_utc = False

# app.conf.update(timezone = "Asia/Kolkata")
# # read config from Django settings, the CELERY namespace would make celery 
# # config keys has `CELERY` prefix
# app.config_from_object(settings, namespace='CELERY')

# # # load tasks.py in django apps
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind = True)
# def debug_task(self):
#    print('Request: {0!r}'.format(self.request))

# # Define a periodic task to check container uptime
# app.conf.beat_schedule = {
#     'check-container-uptime': {
#         'task': 'submission.tasks.check_container_uptime',
#         'schedule': crontab(minute='2'),  # Run every minute
#     },
# }


# *****************************


# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# # setting the Django settings module.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_task.settings')
# app = Celery('NCC')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# # Looks up for task modules in Django applications and loads them
# app.autodiscover_tasks()
