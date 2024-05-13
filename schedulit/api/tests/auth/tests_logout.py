from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status

from schedulit.api.tests.helpers import ApiTestCase, RequestMethods


class LogoutTest(ApiTestCase):
    url_logout: str
    url_logout_all: str

    @classmethod
    def setUpTestData(cls):
        cls.url_logout = reverse('account_logout')
        cls.url_logout_all = reverse('account_logout_all')

    def setUp(self):
        self.initialize_users()
        self.user_tokens = [
            (self.user_token, self.user_token_str),
            AuthToken.objects.create(user=self.user),
            AuthToken.objects.create(user=self.user),
            AuthToken.objects.create(user=self.user)
        ]
        self.set_auth_header(self.user_token_str)

    def test_logout_should_logout_user(self):
        self.assertEqual(AuthToken.objects.filter(user=self.user).count(), len(self.user_tokens))
        self.set_auth_header(self.user_token_str)
        self.assert_post(self.url_logout, None, status.HTTP_200_OK)
        self.assertRaises(AuthToken.DoesNotExist, self.user_token.refresh_from_db)
        self.assertEqual(AuthToken.objects.filter(user=self.user).count(), len(self.user_tokens) - 1)
        # auth token should not be valid anymore
        self.assert_post(self.url_logout, None, status.HTTP_401_UNAUTHORIZED)

    def test_logout_all_should_destroy_all_user_tokens(self):
        self.assertEqual(AuthToken.objects.filter(user=self.user).count(), len(self.user_tokens))
        self.set_auth_header(self.user_token_str)
        self.assert_post(self.url_logout_all, None, status.HTTP_200_OK)
        self.assertRaises(AuthToken.DoesNotExist, self.user_token.refresh_from_db)
        self.assertEqual(AuthToken.objects.filter(user=self.user).count(), 0)
        # auth token should not be valid anymore
        self.assert_post(self.url_logout_all, None, status.HTTP_401_UNAUTHORIZED)

    def test_logout_should_fail_with_invalid_authentication_headers(self):
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.POST, self.url_logout)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.POST, self.url_logout_all)

    def test_logout_should_only_accept_post(self):
        not_accepted_methods = [RequestMethods.GET, RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_logout)
        self.assert_not_allowed_methods(not_accepted_methods, self.url_logout_all)

    def test_logout_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_logout)
        self.assert_should_respond_to_options(self.url_logout_all)
