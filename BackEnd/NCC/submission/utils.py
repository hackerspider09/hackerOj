from .models import *
from contest import models as modelsCo
from django.conf import settings
import redis

crntVM = settings.VM
redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=6379, db=0)

def getContainer():
    container = modelsCo.Container.objects.filter(status=False).exists()
    if container:
        containerId = modelsCo.Container.objects.filter(status=False).first()
        containerId.status = True
        containerId.count+=1
        containerId.save()
        return containerId.containerId
    return False

def deallocate(containerid):
    container = modelsCo.Container.objects.get(containerId=containerid)
    container.status = False
    container.save()

def getActivatedContainer():
    containerQuery = modelsCo.DockerJudgeContainer.objects.get(vm=crntVM)
    activatedContainerNumber = modelsCo.ActivatedContainer.objects.filter(disable=False,vm=containerQuery).count()

    if ( containerQuery.maxNumber>=activatedContainerNumber ):
        return True
    return False


def getExecutionServer():
    try:
        total_submissions = redis_client.incr('total_submissions')
        total_submissions = int(redis_client.get('total_submissions') or 0)
        servers = modelsCo.ExecutionServers.objects.all()
        if not servers:
            return None
        server_index = total_submissions % len(servers)
        selected_server = servers[server_index]
        return {'ip_address': selected_server.address,'port':selected_server.port}
    except Exception as e:
        print(f"Error selecting server: {e}")
        return None