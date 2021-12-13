from afterpay.exceptions.params_error import ParamsError


class ClientTokenGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def generate(self, params=None):
        """
        Generate a client token
        :param params: Request parameters
            :param amount: Total amount for order to be charged to consumer.
                :param amount: The amount as a string representation of a decimal number, rounded to 2 decimal places.
                :param currency: The currency in ISO 4217 format. Supported values include "AUD", "NZD", "USD", and
                "CAD". However, the value provided must correspond to the currency of the Merchant account making
                the request.
            :param consumer: The consumer requesting the order.
                :param givenNames: The consumer’s first name and any middle names. Limited to 128 characters.
                :param surname: The consumer’s last name. Limited to 128 characters.
                :param email: The consumer’s email address. Limited to 128 characters.
                :param phoneNumber?: The consumer’s phone number. Limited to 32 characters.
            :param shipping: Shipping address object
                :param name: Full name of contact. Limited to 255 characters.
                :param line1: First line of the address. Limited to 128 characters.
                :param line2?: Second line of the address. Limited to 128 characters
                :param area1: Australian suburb, New Zealand town or city, U.K. Postal town, U.S. or Canadian city.
                Limited to 128 characters.
                :param area2?: New Zealand suburb or U.K. village or local area. Limited to 128 characters.
                :param region: Australian state, New Zealand region, U.K. county, Canadian Territory or Province,
                or U.S. state. Limited to 128 characters.
                :param postcode: ZIP or postal code. Limited to 128 characters
                :param countryCode: The two-character ISO 3166-1 country code.
                :param phoneNumber?: The phone number, in E.123 format. Limited to 32 characters
            :param merchant: Merchant data
                :param redirectConfirmUrl: Checkout confirmation URL
                :param redirectCancelUrl: Checkout cancellation URL
            :param billing?: Billing address object
            :param courier?: Courier object
            :param items?: An array of order items
            :param discounts?: An array of discounts
        """
        if params is None:
            params = {}
        if "amount" not in params:
            raise ParamsError("Missing required parameter: amount")
        if "consumer" not in params:
            raise ParamsError("Missing required parameter: consumer")
        if "shipping" not in params:
            raise ParamsError("Missing required parameter: shipping")

        # Validate client_token
        params = {'client_token': params}

        response = self.config.http().post(self.config.api_url() + "/checkouts", params)

        if "client_token" in response:
            return response["client_token"]["value"]
        else:
            raise ValueError(response["api_error_response"]["message"])
