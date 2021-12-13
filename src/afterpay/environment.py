import os
import inspect
import certifi

class Environment(object):
    """
    Create an environment
    """

    def __init__(self, name, server, port, is_ssl, ssl_certificate):
        self.__name__ = name
        self.__server = server
        self.__port = port
        self.is_ssl = is_ssl
        self.ssl_certificate = ssl_certificate

    @property
    def base_url(self):
        return "%s%s:%s" % (self.protocol, self.server, self.port)

    @property
    def port(self):
        return int(self.__port)

    @property
    def auth_url(self):
        return self.__auth_url

    @property
    def protocol(self):
        return self.__port == "443" and "https://" or "http://"

    @property
    def server(self):
        return self.__server

    @property
    def server_and_port(self):
        return self.__server + ":" + self.__port

    @staticmethod
    def parse_environment(environment):
        if isinstance(environment, Environment) or environment is None:
            return environment
        try:
            return Environment.All[environment]
        except KeyError as e:
            raise KeyError("Unable to process supplied environment")

    @staticmethod
    def afterpay_root():
        return os.path.dirname(inspect.getfile(Environment))

    def __str__(self):
        return self.__name__

Environment.Sandbox_NA = Environment("sandbox", "api.us-sandbox.afterpay.com", "443", True, certifi.where())
Environment.Sandbox_OC = Environment("sandbox", "api-sandbox.afterpay.com", "443", True, certifi.where())
Environment.Production_NA = Environment("production", "api.us.afterpay.com", "443", True, certifi.where())
Environment.Production_OC = Environment("production", "api.afterpay.com", "443", True, certifi.where())
Environment.All = {
    "sandbox_north_america": Environment.Sandbox_NA,
    "sandbox_oceania": Environment.Sandbox_OC,
    "production_north_america": Environment.Production_NA,
    "production_oceania": Environment.Production_OC
}
