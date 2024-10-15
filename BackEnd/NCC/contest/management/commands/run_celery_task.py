# management/commands/run_celery_task.py
from django.core.management.base import BaseCommand
from submission.tasks import get_Testcases

class Command(BaseCommand):
    help = 'Run the get_Testcases Celery task'

    def handle(self, *args, **options):
        get_Testcases.delay()
        self.stdout.write(self.style.SUCCESS('Celery task get_Testcases has been triggered successfully'))
