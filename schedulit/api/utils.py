import typing

from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication
from rest_framework import status, exceptions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from schedulit.authentication.models import User

if typing.TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from django.utils.functional import _StrPromise


def is_authenticated(user: AnonymousUser | User) -> typing.TypeGuard[User]:
    return bool(user and user.is_authenticated)


# class IsEmployeeAuthenticated(IsAuthenticated):
#     def has_permission(self, request: Request, _view: APIView) -> bool:
#         user = request.user
#         return bool(is_authenticated(user) and user.is_employee)
#

class IsSchedulerAuthenticated(IsAuthenticated):

    def has_permission(self, request: Request, _view: APIView) -> bool:
        user = request.user
        return bool(is_authenticated(user) and user.is_scheduler)


class BaseApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def _response(data: dict[typing.Any, typing.Any], message: '_StrPromise | None', headers: dict[str, str] | None,
                  status_code: int) -> Response:
        response_content = {}
        response_content.update(data)
        if message:
            response_content['message'] = message

        response = Response(response_content, headers=headers, status=status_code)
        return response

    def success_response(self, data: dict[typing.Any, typing.Any], message: '_StrPromise' = None,
                         headers: dict[str, str] = None) -> Response:
        return self._response(data=data, message=message, headers=headers, status_code=status.HTTP_200_OK)


class BaseSchedulerView(APIView):
    permission_classes = [IsSchedulerAuthenticated]


# class BaseEmployeeView(APIView):
#     permission_classes = [IsEmployeeAuthenticated]
#

class Catchall404View(BaseApiView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def initial(self, request, *args, **kwargs):
        # This view will return NotFound() allways!!
        raise exceptions.NotFound(request.path)
