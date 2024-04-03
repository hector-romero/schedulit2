from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from knox import views as knox_views
from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.utils import BaseApiView


# https://jazzband.github.io/django-rest-knox/auth/
class LoginView(knox_views.LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):  # pylint: disable=redefined-builtin
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=format)


class LogoutView(BaseApiView, knox_views.LogoutView):
    def post(self, request, format=None):  # pylint: disable=redefined-builtin
        super().post(request, format=format)
        return self.success_response({}, _('Logged out successfully.'))


class LogoutAllView(BaseApiView, knox_views.LogoutAllView):
    def post(self, request, format=None):  # pylint: disable=redefined-builtin
        super().post(request, format=format)
        return self.success_response({}, _('Logged out from all devices successfully.'))


class UserProfileView(BaseApiView):
    def get(self, request):
        return self.success_response({'user': UserSerializer(request.user).data})


class RegisterView(generics.CreateAPIView, LoginView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        login(request, serializer.instance)
        return super(LoginView, self).post(request, format=None)
