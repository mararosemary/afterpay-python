import uuid
from afterpay.exceptions.afterpay_error import AfterpayError
from afterpay.exceptions.params_error import ParamsError
from afterpay.exceptions.payment_error import PaymentError

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
            :param token: The client token generated from a checkout flow
            :param merchantReference?: The merchant’s order ID/reference that this payment corresponds to.
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
        :param refund_id: Internal refund ID, different from requestId
        :param params: Request parameters
            :param amount: The refund amount. The refund amount can not exceed the payment total.
                :param amount: The amount as a string representation of a decimal number, rounded to 2 decimal places.
                :param currency: The currency in ISO 4217 format. Supported values include "AUD", "NZD", "USD", and
                "CAD". However, the value provided must correspond to the currency of the Merchant account making
                the request.
            :param requestId?: A unique request ID, required for safe retries.
            It is recommended that the merchant generate a UUID for each unique refund.
            :param merchantReference?: The merchant’s internal refund id/reference. This must be included
            along with the requestId to utilise idempotency.
            :param refundMerchantReference?: A unique reference for the individual refund event. If provided,
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
