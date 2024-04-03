from rest_framework.status import HTTP_200_OK


# Allow CORS request for api request.
# for now, using * for allowed-origins
class APIMiddleWare:  # pylint: disable=too-few-public-methods
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_path = "/api/"

    def __call__(self, request):
        # Add the account attribute to all the requests for api to avoid having
        # to do the check hasattr(request, 'account')

        response = self.get_response(request)
        if request.path.startswith(self.api_path):
            # Handling the preflight OPTIONS and return allways 200
            if request.method == 'OPTIONS':
                response.status_code = HTTP_200_OK
            response["Access-Control-Allow-Methods"] = "*"  # "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "*"
            response["Access-Control-Allow-Origin"] = "*"
        return response
