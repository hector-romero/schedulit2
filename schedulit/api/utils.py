from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class IsEmployeeAuthenticated(IsAuthenticated):
    def has_permission(self, request, view: APIView) -> bool:
        is_authenticated = super().has_permission(request, view)
        # noinspection PyUnresolvedReferences
        return bool(is_authenticated and request.user.is_employee)


class IsSchedulerAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        # noinspection PyUnresolvedReferences
        return bool(is_authenticated and request.user.is_scheduler)


class BaseApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    authentication_classes = [TokenAuthentication]
    error_response_status_code = status.HTTP_400_BAD_REQUEST

    @staticmethod
    def _response(data: dict, message: str | None, headers: dict | None, status_code: int) -> Response:
        response_content = {}
        response_content.update(data)
        if message:
            response_content['message'] = message

        response = Response(response_content, headers=headers, status=status_code)
        return response

    def success_response(self, data: dict, message: str = None, headers: dict = None) -> Response:
        return self._response(data=data, message=message, headers=headers, status_code=status.HTTP_200_OK)

    def error_response(self, data: dict, message: str = None, headers: dict = None) -> Response:
        return self._response(data=data, message=message, headers=headers, status_code=self.error_response_status_code)


class BaseSchedulerView(APIView):
    permission_classes = [IsSchedulerAuthenticated]


class BaseEmployeeView(APIView):
    permission_classes = [IsEmployeeAuthenticated]
