import base64
import typing
from enum import Enum

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from knox.models import AuthToken
from model_bakery import baker
from rest_framework import status

from schedulit.authentication.models import User

if typing.TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from django.test.client import _MonkeyPatchedWSGIResponse


class RequestMethods(Enum):
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    GET = 'get'


RequestMethodWithBody = typing.Literal[
    RequestMethods.POST, RequestMethods.PUT, RequestMethods.PATCH, RequestMethods.DELETE]


class ApiTestCase(TestCase):
    user: User
    user2: User
    user_token: AuthToken
    user2_token: AuthToken
    user_token_str: str
    user2_token_str: str
    headers: dict[str, str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {}

    @classmethod
    def initialize_users(cls) -> None:
        # Creates two users, with the password "password"
        cls.user = baker.make(User, password=make_password('password'), role=User.Roles.SCHEDULER)
        cls.user2 = baker.make(User, password=make_password('password'), role=User.Roles.EMPLOYEE)

        cls.user_token, cls.user_token_str = AuthToken.objects.create(user=cls.user)
        cls.user2_token, cls.user2_token_str = AuthToken.objects.create(user=cls.user2)

    def set_headers(self, headers: dict[str, str]) -> None:
        self.headers = headers

    def set_auth_header(self, token: str | None) -> None:
        if not token:
            self.headers.pop('AUTHORIZATION', None)
        else:
            self.headers['AUTHORIZATION'] = 'Token ' + token

    def assert_response_cors(self, response: '_MonkeyPatchedWSGIResponse') -> None:
        # Makes sure that the response has the CORS headers set to '*' (not ideal, but it works)
        self.assertEqual(response.headers.get("Access-Control-Allow-Methods"), "*")
        self.assertEqual(response.headers.get("Access-Control-Allow-Headers"), "*")
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")

    def assert_json_response(self, response: '_MonkeyPatchedWSGIResponse', http_status_code: int,
                             error_type: str | None) -> typing.Any:
        self.assert_response_cors(response)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response_json = {}
        else:
            response_json = response.json()

        # Show the error received in case of getting an unexpected test case fail
        # pragma: no cover
        if response.status_code != http_status_code or \
                (error_type and response_json.get('type') != error_type):  # pragma: no cover
            print("##### ASSERT RESPONSE FAIL  #######")
            print(http_status_code, error_type)
            print(response.status_code, response_json)
            print("###################################")
        if error_type:
            self.assertEqual(response_json.get('type'), error_type)
        self.assertEqual(response.status_code, http_status_code)
        return response_json

    def _assert_request_with_json_body(self, method: RequestMethodWithBody, url: str, json_params: typing.Any,
                                       http_status_code: int, error_type: str = None) -> typing.Any:
        client_method = getattr(self.client, method.value)
        response = client_method(url, json_params, content_type='application/json', headers=self.headers)
        return self.assert_json_response(response, http_status_code, error_type)

    def assert_post(self, url: str, json_params: typing.Any, http_status_code: int,
                    error_type: str = None) -> typing.Any:
        return self._assert_request_with_json_body(
            RequestMethods.POST, url, json_params, http_status_code, error_type)

    def assert_put(self, url: str, json_params: typing.Any, http_status_code: int) -> typing.Any:
        return self._assert_request_with_json_body(RequestMethods.PUT, url, json_params, http_status_code)

    def assert_patch(self, url: str, json_params: typing.Any, http_status_code: int) -> typing.Any:
        return self._assert_request_with_json_body(RequestMethods.PATCH, url, json_params, http_status_code)

    def assert_delete(self, url: str, http_status_code: int) -> typing.Any:
        return self._assert_request_with_json_body(RequestMethods.DELETE, url, {}, http_status_code)

    def assert_get(self, url: str, http_status_code: int, data: dict[str, str] = None, error_type: str = None) \
            -> typing.Any:
        response = self.client.get(url, data=data, headers=self.headers)
        return self.assert_json_response(response, http_status_code, error_type)

    # Invalid authentication header tests
    def assert_invalid_authentication_header_tests_for_method(self, method: RequestMethods, url: str,
                                                              json_params: typing.Any = None) -> None:
        if method == RequestMethods.GET:
            def _assertion() -> None:
                self.assert_get(url, status.HTTP_401_UNAUTHORIZED)
        else:
            def _assertion() -> None:
                self._assert_request_with_json_body(method, url, json_params, status.HTTP_401_UNAUTHORIZED)

        # should fail if no authorization header is set
        self.set_auth_header(None)
        _assertion()

        # should fail if invalid authorization header is set
        self.set_headers({'AUTHORIZATION': 'Token <some_invalid_authorization_token>'})
        _assertion()

        self.set_headers({'AUTHORIZATION': '<some_invalid_authorization_token>'})
        _assertion()

        # Missing token
        self.set_headers({'AUTHORIZATION': 'Token'})
        _assertion()

        # Missing "Token " prefix
        self.set_headers({'AUTHORIZATION': self.user_token_str})
        _assertion()

        # should fail if attempting to use a different authentication method
        credentials = base64.b64encode(bytes(self.user.email + ":password", "utf-8")).decode('utf-8')
        self.set_headers(
            {'AUTHORIZATION': f'Basic ${credentials}'})
        _assertion()

    # Invalid json tests
    def assert_invalid_json_params(self, method: RequestMethodWithBody, url: str) -> None:
        possibilities = [
            ('{ldd}', 'invalid_request'),
            ('{"password": some_pass, email: some@email.com}', 'invalid_request'),
            # No data provided
            ('null', 'validation_error'),

            # strings that could be parsed as valid json, still shouldn't be accepted
            ('some string', 'invalid_request'),
            ('1', 'validation_error'),
            ('true', 'validation_error'),
            ('[]', 'validation_error'),

        ]

        for invalid_json, error_type in possibilities:
            self._assert_request_with_json_body(method, url, invalid_json, status.HTTP_400_BAD_REQUEST,
                                                error_type=error_type)

    def assert_not_allowed_methods(self, methods: typing.List[RequestMethods], url: str) -> None:
        for method in methods:
            if method == RequestMethods.GET:
                self.assert_get(url, status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                self._assert_request_with_json_body(method, url, {}, status.HTTP_405_METHOD_NOT_ALLOWED)

    def assert_should_respond_to_options(self, url: str) -> None:
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_response_cors(response)
