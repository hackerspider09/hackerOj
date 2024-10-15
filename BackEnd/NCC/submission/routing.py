from django.urls import re_path
from submission import consumers

websocket_urlpatterns = [
    re_path(r"^ws/submission/(?P<submission_id>[^/]+)/$", consumers.SubmissionConsumer.as_asgi()),
]
