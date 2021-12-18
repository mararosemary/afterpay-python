import requests
import json
from base64 import encodebytes
from afterpay import version
from afterpay.exceptions.authentication_error import AuthenticationError
from afterpay.exceptions.invalid_request import InvalidRequestError
from afterpay.exceptions.invalid_headers import InvalidHeadersError
from afterpay.exceptions.invalid_method import InvalidMethodError
from afterpay.exceptions.params_error import ParamsError
from afterpay.exceptions.payment_error import PaymentError
from afterpay.exceptions.payment_not_found_error import PaymentNotFoundError
from afterpay.exceptions.server_error import ServerError
from afterpay.exceptions.token_error import TokenError
from afterpay.exceptions.unexpected_error import UnexpectedError
from afterpay.exceptions.http.connection_error import ConnectionError
from afterpay.exceptions.http.timeout_error import ConnectTimeoutError
from afterpay.exceptions.http.invalid_response_error import InvalidResponseError
from afterpay.exceptions.http.timeout_error import ReadTimeoutError
from afterpay.exceptions.http.timeout_error import TimeoutError

class Http(object):
    class ContentType(object):
        Json = "application/json"

    @staticmethod
    def is_error_status(status):
        return status not in [200, 201]

    @staticmethod
    def raise_exception_from_status(status, message=None):
        if status == 400:
            raise InvalidRequestError()
        elif status == 401:
            raise AuthenticationError()
        elif status == 402:
            raise TokenError()
        elif status == 404:
            raise PaymentNotFoundError()
        elif status == 405:
            raise InvalidMethodError()
        elif status == 406:
            raise InvalidHeadersError()
        elif status == 412:
            raise PaymentError()
        elif status == 415:
            raise InvalidHeadersError()
        elif status == 422:
            raise ParamsError(message)
        elif status == 500:
            raise ServerError()
        else:
            raise UnexpectedError("Unexpected HTTP_RESPONSE " + str(status))

    def __init__(self, config, environment=None):
        self.config = config
        self.environment = environment or self.config.environment

    def post(self, path, params=None):
        return self._make_request("POST", path, Http.ContentType.Json, params)

    def delete(self, path):
        return self._make_request("DELETE", path, Http.ContentType.Json)

    def get(self, path):
        return self._make_request("GET", path, Http.ContentType.Json)

    def put(self, path, params=None):
        return self._make_request("PUT", path, Http.ContentType.Json, params)

    def _make_request(self, http_verb, path, content_type, params=None, files=None, header_overrides=None):
        http_strategy = self.config.http_strategy()
        headers = self.__headers(header_overrides)
        request_body = self.__request_body(content_type, params, files)

        try:
            status, response_body = http_strategy.http_do(http_verb, path, headers, request_body)
        except Exception as e:
            if self.config.wrap_http_exceptions:
                http_strategy.handle_exception(e)
            else:
                raise

        if Http.is_error_status(status):
            Http.raise_exception_from_status(status)
        else:
            if len(response_body.strip()) == 0:
                return {}
            else:
                if content_type == Http.ContentType.Json:
                    return json.loads(response_body)

    def http_do(self, http_verb, path, headers, request_body):
        data = request_body
        files = None

        if type(request_body) is tuple:
            data = request_body[0]
            files = request_body[1]

        verify = self.environment.ssl_certificate

        response = self.__request_function(http_verb)(
            path,
            headers=headers,
            data=data,
            files=files,
            verify=verify,
            timeout=self.config.timeout
        )

        return [response.status_code, response.text]

    def handle_exception(self, exception):
        if isinstance(exception, requests.exceptions.ReadTimeout):
            raise ReadTimeoutError(exception)
        elif isinstance(exception, requests.exceptions.ConnectTimeout):
            raise ConnectTimeoutError(exception)
        elif isinstance(exception, requests.exceptions.ConnectionError):
            raise ConnectionError(exception)
        elif isinstance(exception, requests.exceptions.HTTPError):
            raise InvalidResponseError(exception)
        elif isinstance(exception, requests.exceptions.Timeout):
            raise TimeoutError(exception)
        else:
            raise UnexpectedError(exception)

    def __request_function(self, method):
        if method == "GET":
            return requests.get
        elif method == "POST":
            return requests.post
        elif method == "PUT":
            return requests.put
        elif method == "DELETE":
            return requests.delete

    def __authorization_header(self):
        return b"Basic " + encodebytes(
                    self.config.merchant_id.encode('ascii') +
                    b":" +
                    self.config.secret_key.encode('ascii')
                ).replace(b"\n", b"").strip()

    def __headers(self, header_overrides=None):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.__authorization_header(),
            "User-Agent": "Python Afterpay Library " + version.Version,
        }

        headers.update(header_overrides or {})

        return headers

    def __request_body(self, content_type, params, files):
        if content_type == Http.ContentType.Json:
            request_body = json.dumps(params) if params else ''
            return request_body
        elif files == None:
            return params
        else:
            return (params, files)
