from django.contrib.auth.backends import BaseBackend
from .models import Manager

class ManagerAuthBackend(BaseBackend):
    def authenticate(self, request, mgr_id=None, password=None):
        try:
            manager = Manager.objects.get(mgr_id=mgr_id)
            if manager.password == password:
                return manager
        except Manager.DoesNotExist:
            return None

    def get_user(self, mgr_id):
        try:
            return Manager.objects.get(pk=mgr_id)
        except Manager.DoesNotExist:
            return None
