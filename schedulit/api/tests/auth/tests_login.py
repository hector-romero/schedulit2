from django.contrib.auth.hashers import make_password
from django.urls import reverse
from knox.auth import TokenAuthentication
from model_bakery import baker
from rest_framework import status

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods

from schedulit.authentication.models import User
from schedulit.utils.tests.helpers import same_email_variations


def get_login_params(username: str | None, password: str | None) -> dict[str, str | None]:
    return {"username": username, "password": password}


class LoginTest(ApiTestCase):
    url_login: str

    @classmethod
    def setUpTestData(cls):
        cls.url_login = reverse('account_login')
        cls.user, cls.user2 = baker.make(User, _quantity=2, password=make_password('password'))

    def test_should_allow_user_login_with_correct_credentials_and_return_valid_user_token(self):
        # should return token for valid credentials.
        for user in [self.user, self.user2]:
            # Ensures that the user password is known
            response = self.assert_post(self.url_login, get_login_params(user.email, 'password'),
                                        status.HTTP_200_OK)
            user.refresh_from_db()

            self.assertIsNotNone(response['token'])

            # The token should be linked to the user
            user_from_token, _ = TokenAuthentication().authenticate_credentials(response['token'].encode())
            self.assertEqual(user, user_from_token)

            self.assertEqual(response['user'], UserSerializer(instance=user).data)

    def test_login_should_be_case_insensitive_for_email(self):
        user = baker.make(User, password=make_password('password'), email=same_email_variations[0])
        for email in same_email_variations:
            response = self.assert_post(self.url_login, get_login_params(email, 'password'),
                                        status.HTTP_200_OK)
            self.assertEqual(user.email, response['user']['email'])

    def test_login_should_fail_with_invalid_or_missing_password(self):
        # TODO Should we fail with another status code?
        self.assert_post(self.url_login, get_login_params(self.user.email, 'PASSWORD'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params(self.user.email, 'invalid_password'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params(self.user.email, None),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params(self.user.email, ''),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, {'username': self.user.email}, status.HTTP_400_BAD_REQUEST)

    def test_login_should_fail_with_invalid_or_missing_email(self):
        self.assert_post(self.url_login, get_login_params("invalid" + self.user.email, 'password'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params('invalid_email', 'password'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params('', 'password'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, get_login_params(None, 'password'),
                         status.HTTP_400_BAD_REQUEST)

        self.assert_post(self.url_login, {'password': 'password'},
                         status.HTTP_400_BAD_REQUEST)

    def test_login_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.POST, self.url_login)

    def test_login_should_only_accept_post(self):
        not_accepted_methods = [RequestMethods.GET, RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_login)

    def test_login_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_login)
