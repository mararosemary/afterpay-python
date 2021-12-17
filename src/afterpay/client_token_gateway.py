from afterpay.exceptions.params_error import ParamsError


class ClientTokenGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def generate(self, params=None):
        """
        Generate a client token
        :param params: Request parameters
            amount: Total amount for order to be charged to consumer.
                amount: The amount as a string representation of a decimal number, rounded to 2 decimal places.
                currency: The currency in ISO 4217 format. Supported values include "AUD", "NZD", "USD", and
                "CAD". However, the value provided must correspond to the currency of the Merchant account making
                the request.
            consumer: The consumer requesting the order.
                givenNames: The consumer’s first name and any middle names. Limited to 128 characters.
                surname: The consumer’s last name. Limited to 128 characters.
                email: The consumer’s email address. Limited to 128 characters.
                phoneNumber?: The consumer’s phone number. Limited to 32 characters.
            shipping: Shipping address object
                name: Full name of contact. Limited to 255 characters.
                line1: First line of the address. Limited to 128 characters.
                line2?: Second line of the address. Limited to 128 characters
                area1: Australian suburb, New Zealand town or city, U.K. Postal town, U.S. or Canadian city.
                Limited to 128 characters.
                area2?: New Zealand suburb or U.K. village or local area. Limited to 128 characters.
                region: Australian state, New Zealand region, U.K. county, Canadian Territory or Province,
                or U.S. state. Limited to 128 characters.
                postcode: ZIP or postal code. Limited to 128 characters
                countryCode: The two-character ISO 3166-1 country code.
                phoneNumber?: The phone number, in E.123 format. Limited to 32 characters
            merchant: Merchant data
                redirectConfirmUrl: Checkout confirmation URL
                redirectCancelUrl: Checkout cancellation URL
            billing?: Billing address object
            courier?: Courier object
            items?: An array of order items
            discounts?: An array of discounts
        """
        if params is None:
            params = {}

        if "amount" not in params:
            raise ParamsError("Amount does not exist or is invalid")
        if "amount" not in params["amount"]:
            raise ParamsError("Amount does not exist or is invalid")
        if "currency" not in params["amount"]:
            raise ParamsError("Amount does not exist or is invalid")
        if params["amount"]["currency"] not in ["AUD", "NZD", "USD", "CAD"]:
            raise ParamsError("Invalid currency in Amount object")

        if "consumer" not in params:
            raise ParamsError("Consumer object does not exist or is invalid")
        if "email" not in params["consumer"]:
            raise ParamsError("Consumer object does not exist or is invalid")
        if "givenNames" not in params["consumer"]:
            raise ParamsError("Consumer object does not exist or is invalid")
        if "surname" not in params["consumer"]:
            raise ParamsError("Consumer object does not exist or is invalid")

        if "shipping" not in params:
            raise ParamsError("Shipping does not exist or is invalid")
        if "name" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")
        if "line1" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")
        if "area1" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")
        if "region" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")
        if "postcode" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")
        if "countryCode" not in params["shipping"]:
            raise ParamsError("Shipping does not exist or is invalid")

        return self.config.http().post(self.config.api_url() + "/checkouts/", params)