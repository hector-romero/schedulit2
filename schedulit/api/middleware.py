import typing

from django.http import HttpResponse, HttpRequest


# Allow CORS request for api request.
# for now, using * for allowed-origins
class APIMiddleWare:  # pylint: disable=too-few-public-methods
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_path = "/api/"

    @staticmethod
    def set_cors_headers(response: HttpResponse) -> None:
        response["Access-Control-Allow-Methods"] = "*"  # "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Origin"] = "*"

    def __call__(self, request: HttpRequest) -> typing.Any:
        # Add the account attribute to all the requests for api to avoid having
        # to do the check hasattr(request, 'account')

        if request.path.startswith(self.api_path):
            if request.method == 'OPTIONS':
                response = HttpResponse(headers={"content-length": "0", "content-type": "application/json"})
            else:
                response = self.get_response(request)
            self.set_cors_headers(response)
            return response
        return self.get_response(request)
