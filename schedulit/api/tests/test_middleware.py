from unittest import mock

from django.http import HttpResponse
from django.test import TestCase

from schedulit.api.middleware import APIMiddleWare


class MiddlewareTest(TestCase):

    def test_api_middleware_set_cors_headers_should_set_cors_for_a_response(self):
        response = HttpResponse(headers=None)
        APIMiddleWare.set_cors_headers(response)
        self.assertEqual(response.headers.get("Access-Control-Allow-Methods"), "*")
        self.assertEqual(response.headers.get("Access-Control-Allow-Headers"), "*")
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")

    @mock.patch('schedulit.api.middleware.APIMiddleWare.set_cors_headers')
    def test_api_middleware_should_set_cors_headers_for_api_calls(self, mock_set_cors_headers):
        mock_set_cors_headers.assert_not_called()
        self.client.options('/api/')
        mock_set_cors_headers.assert_called()

    @mock.patch('schedulit.api.middleware.APIMiddleWare.set_cors_headers')
    def test_api_middleware_should_not_return_cors_headers_for_non_api_endpoints(self, mock_set_cors_headers):
        mock_set_cors_headers.assert_not_called()
        self.client.options('/')
        mock_set_cors_headers.assert_not_called()
