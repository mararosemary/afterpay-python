from afterpay.attribute_getter import AttributeGetter
from afterpay.exceptions import AfterpayError


class Money(AttributeGetter):
    """
    Money object
    Attributes:
        amount: The amount is a string representation of a decimal number, rounded to 2 decimal places.
        currency: The currency in ISO 4217 format. Supported values include "AUD", "NZD", "USD", and "CAD".
        However, the value provided must correspond to the currency of hte Merchant account making the request.
        This class does not validate if the Money object currency matches the Merchant account currency.
    """
    attribute_list = [
        "amount",
        "currency",
    ]

    def __init__(self, attributes):
        if "amount" not in attributes:
            raise AfterpayError("Cannot initialize Money object without an 'amount'")
        if "currency" not in attributes:
            raise AfterpayError("Cannot initialize Money object without a 'currency'")

        AttributeGetter.__init__(self, attributes)

        if self.currency not in ["AUD", "NZD", "USD", "CAD"]:
            raise AfterpayError("Cannot initialize Money object with an invalid currency")

        if isinstance(self.amount, int) or isinstance(self.amount, float):
            self.amount = str(round(self.amount, 2))

    def __repr__(self):
        return super(Money, self).__repr__(self.attribute_list)

    def get_json(self):
        return {
            i: super(Money, self).__dict__[i] for i in super(Money, self).__dict__ if i in self.attribute_list
        }
