from django.core.management.base import BaseCommand
from django.utils import timezone
from contest.models import Container  

class Command(BaseCommand):
    help = 'Create 12 instances of the Judge Container model'

    def handle(self, *args, **options):
        # Create 12 Container instances
        for i in range(1, 13):
            container_id = i
            if not Container.objects.filter(containerId=container_id).exists():
                Container.objects.create(
                    containerId=container_id,
                )

                self.stdout.write(self.style.SUCCESS(f'Container {container_id} created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Container {container_id} already exists'))