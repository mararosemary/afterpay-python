from afterpay.attribute_getter import AttributeGetter
from afterpay.exceptions import AfterpayError


class Merchant(AttributeGetter):
    """
    Merchant object
    Attributes:
        redirectConfirmUrl: The consumer is redirected to this URL when the payment process is completed.
        redirectCancelUrl: The consumer is redirected to this URL if the payment process is cancelled.
    """
    attribute_list = [
        "redirectConfirmUrl",
        "redirectCancelUrl",
    ]

    def __init__(self, attributes):
        if "redirectConfirmUrl" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'redirectConfirmUrl'")
        if "redirectCancelUrl" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'redirectCancelUrl'")

        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(Merchant, self).__repr__(self.attribute_list)

    def get_json(self):
        return {
            i: super(Merchant, self).__dict__[i] for i in super(Merchant, self).__dict__ if i in self.attribute_list
        }
