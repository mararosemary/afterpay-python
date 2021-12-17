import uuid
# from afterpay.consumer import Consumer
# from afterpay.contact import Contact
# from afterpay.merchant import Merchant
# from afterpay.money import Money
from afterpay.exceptions.afterpay_error import AfterpayError
from afterpay.exceptions.params_error import ParamsError
# from afterpay.exceptions.payment_error import PaymentError


class Payment(object):
    """
    Manage immediate Payment flow
    """

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config
        self.payments_url = self.config.api_url() + "/payments"

    def capture(self, params=None):
        """
        This operation is idempotent based on the token,
        which allows for the safe retry of requests,
        guaranteeing the payment operation is only performed once.
        :param: Request parameters
            token: The client token generated from a checkout flow
            merchantReference?: The merchant’s order ID/reference that this payment corresponds to.
            This will update any value previously provided in the checkout flow
        """
        if params is None:
            params = {}
        if "token" not in params:
            raise ParamsError("Missing required parameter: client_token")
        if "amount" in params:
            raise AfterpayError("Express checkout not supported")

        return self.config.http().post(self.payments_url + "/capture/", params)

    def refund(self, order_id=None, params=None, idempotency=True):
        """
        The refund operation is idempotent if a unique requestId and merchantReference are provided.
        :param order_id: Order ID to refund
        :param params: Request parameters
            amount: Amount object. The refund amount. The refund amount can not exceed the payment total.
            requestId?: A unique request ID, required for safe retries.
            It is recommended that the merchant generate a UUID for each unique refund.
            merchantReference?: The merchant’s internal refund id/reference. This must be included
            along with the requestId to utilise idempotency.
            refundMerchantReference?: A unique reference for the individual refund event. If provided,
            the value will appear in the daily settlement file as "Payment Event ID". Limited to 128 characters.
        :param idempotency: Set to False to disable idempotency
        """
        if order_id is None:
            raise AfterpayError("Cannot issue refund without an order_id")
        if params is None:
            params = {}
        if "merchantReference" not in params and idempotency:
            raise AfterpayError("Cannot issue refund without merchantReference parameter while idempotency is enabled")
        if "amount" not in params:
            raise ParamsError("Missing required parameter: amount")

        params.requestId = self.generate_uuid()

        return self.config.http().post(self.payments_url + "/" + order_id + "/refund/", params)
