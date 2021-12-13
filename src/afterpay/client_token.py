from afterpay.configuration import Configuration

class ClientToken(object):
    @staticmethod
    def generate(params=None, gateway=None):
        if params is None:
            params = {}
        if gateway is None:
            gateway = Configuration.gateway().client_token

        return gateway.generate(params)