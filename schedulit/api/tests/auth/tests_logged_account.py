from django.urls import reverse
from rest_framework import status

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods


class LoggedAccountTest(ApiTestCase):
    url_logged_account: str

    @classmethod
    def setUpTestData(cls):
        cls.url_logged_account = reverse('account')
        cls.initialize_users()

    def setUp(self):
        self.set_auth_header(self.user_token_str)

    def test_account_endpoint_should_return_logged_in_user(self):
        for user, token_str in [(self.user, self.user_token_str), (self.user2, self.user2_token_str)]:
            self.set_auth_header(token_str)
            response = self.assert_get(self.url_logged_account, status.HTTP_200_OK)
            self.assertEqual(response['user'], UserSerializer(instance=user).data)
            # This endpoint should not return a login token
            self.assertIsNone(response.get('token'))

    def test_account_should_fail_with_invalid_authentication_headers(self):
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.GET, self.url_logged_account)

    def test_account_should_only_accept_get(self):
        not_accepted_methods = [RequestMethods.POST, RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_logged_account)

    def test_account_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_logged_account)
