from rest_framework.viewsets import ModelViewSet

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.utils import BaseSchedulerView
from schedulit.authentication.models import User


class UsersView(ModelViewSet[User], BaseSchedulerView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
