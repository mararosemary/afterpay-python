from afterpay.configuration import Configuration
from afterpay.client_token_gateway import ClientTokenGateway


class AfterpayGateway(object):
    def __init__(self, config=None, **kwargs):
        if isinstance(config, Configuration):
            self.config = config
        else:
            self.config = Configuration(
                http_strategy=kwargs.get("http_strategy")
            )
        self.client_token = ClientTokenGateway(self)
