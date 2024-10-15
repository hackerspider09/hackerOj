from .models import *
from django.conf import settings
import requests

print(settings.MAIN_SERVER_URL)

def callBackApiFunction(submission):
    # Make the request to Server B's Callback API
    payload = {
        'id':submission.id,
        'submissionId': submission.submissionId,
        'mode': submission.mode,
        'status': submission.status,
        'input': submission.input,
        'output': submission.output,
        'error': submission.error,
        'isCorrect': submission.isCorrect,
        'correctSubmissions': submission.correctSubmissions,
        'totalSubmissions': submission.totalSubmissions
    }
    try:
        response = requests.post(f"{settings.MAIN_SERVER_URL}/submission/updatesubmission/", data=payload)
        print(response)
        if response.status_code == 200:
            print("Successfully updated submission on Main server")
        else:
            print(f"Failed to update submission on Main Server: {response.text}")
    except Exception as e:
        print(f"Request to Main server failed: {e}")    


def callBackForInform(submission):
    # Make the request to Server B's Callback API
    payload = {
        'submissionId': submission.submissionId,
    }
    try:
        response = requests.post(f"{settings.MAIN_SERVER_URL}/submission/startsubmission/", data=payload)
        print(response)
        if response.status_code == 200:
            print("Successfully inform about submission on Main server")
        else:
            print(f"Failed to inform about submission on Main Server: {response.text}")
    except Exception as e:
        print(f"Request to Main server failed: {e}")    


