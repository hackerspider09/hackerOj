from rest_framework import permissions
from contest import models as modelsCo

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class RegistrationOpenPermission(permissions.BasePermission):
    message = "Contest has not started yet."

    def has_permission(self, request, view):
        try:
            try:
                contestQuery = modelsCo.Contest.objects.get(contestId=view.kwargs["contestId"])
            except:
                self.message = "Contest Does not Exists."
                return False
            
            if contestQuery.registrationOpen == False:
                self.message = "Registrations are closed."
                return False
            
            return True
        except:
            return False
