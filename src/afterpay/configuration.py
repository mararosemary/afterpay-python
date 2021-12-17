import afterpay
from afterpay.environment import Environment
from afterpay.exceptions.configuration_error import ConfigurationError
from afterpay.util.http import Http


class Configuration(object):
    """
    Create a configuration object

    Example use
        afterpay.Configuration.configure(
            afterpay.Environment.Sandbox_NA,
            "merchant_id",
            "secret_key"
        )
    """

    @staticmethod
    def configure(environment, merchant_id, secret_key, **kwargs):
        """
        :param environment: Environment to use
        :param merchant_id: Afterpay merchant ID
        :param secret_key: Afterpay secret key
        :param kwargs:
            http_strategy: Class to make requests
            timeout: Seconds before a request times out
            wrap_http_exceptions: Return detailed exception
        """
        Configuration.environment = Environment.parse_environment(environment)
        Configuration.merchant_id = merchant_id
        Configuration.secret_key = secret_key
        Configuration.default_http_strategy = kwargs.get("http_strategy", None)
        Configuration.timeout = kwargs.get("timeout", 60)
        Configuration.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)

    @staticmethod
    def gateway():
        return afterpay.gateway.AfterpayGateway(config=Configuration.instantiate())

    @staticmethod
    def instantiate():
        return Configuration(
            environment=Configuration.environment,
            merchant_id=Configuration.merchant_id,
            secret_key=Configuration.secret_key,
            http_strategy=Configuration.default_http_strategy,
            timeout=Configuration.timeout,
            wrap_http_exceptions=Configuration.wrap_http_exceptions
        )

    @staticmethod
    def api_version():
        return "v2"

    def __init__(self, environment=None, merchant_id=None, secret_key=None, *args, **kwargs):
        if len(args) == 2:
            secret_key = args

        self.environment = Environment.parse_environment(environment)
        if merchant_id == "":
            raise ConfigurationError("Missing merchant_id")
        else:
            self.merchant_id = merchant_id

        if secret_key == "":
            raise ConfigurationError("Missing secret key")
        else:
            self.secret_key = secret_key

        self.timeout = kwargs.get("timeout", 60)
        self.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)

        http_strategy = kwargs.get("http_strategy", None)

        if http_strategy:
            self._http_strategy = http_strategy(self, self.environment)
        else:
            self._http_strategy = self.http()

        self.payment_limits = self.get_payment_limits()

    def api_url(self):
        return self.environment.protocol + self.environment.server_and_port + "/" + self.api_version()

    def http(self):
        return Http(self)

    def http_strategy(self):
        return self._http_strategy

    def get_payment_limits(self):
        return self.http().get(self.api_url() + "/configuration")
