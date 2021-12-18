import uuid
import json
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

    def get(self, order_id=None):
        """
        This operation retrieves an individual payment along with its order details.
        :param order_id: Order ID to retrieve
        """
        if order_id is None:
            raise AfterpayError("Cannot retrieve payment without an 'order_id'")

        return self.config.http().get(self.payments_url + "/" + order_id)

    def get_by_token(self, token=None):
        """
        This operation retrieves an individual payment along with its order details.
        :param order_id: Order ID to retrieve
        """
        if token is None:
            raise AfterpayError("Cannot retrieve payment without a 'token'")

        return self.config.http().get(self.payments_url + "/token:" + token)

    def list(self, params=None):
        """
        This operation retrieves an individual payment along with its order details.
        :param params: Request parameters
            toCreatedDate?: An inclusive end date and time to search, in ISO 8601 format.
            fromCreatedDate?: An inclusive start date and time to search, in ISO 8601 format.
            limit?: The number of results to retrieve. Must be between 1 and 250 (inclusive).
            offset?: The position to start the results at. The first result has a position of 0.
            tokens?: One or more order tokens to search for.
            ids?: One or more Afterpay Order IDs to search for.
            merchantReferences?: One or more Merchant Reference IDs to search for.
            statuses?: One or more Afterpay Order Statuses to search for. Possible values include
            "APPROVED" and "DECLINED".
            orderBy?: A field to order results by. If provided, must be one of "createdAt", "id",
            "totalAmount", "merchantReference" or "email".
            ascending?: true to order results in ascending order, or false for descending order.
        """
        if params is None:
            params = {}

        query = "?"
        for key in params:
            if query == "?":
                query = query + key + "=" + params[key]
            else:
                query = query + "&" + key + "=" + params[key]

        return self.config.http().get(self.payments_url + query)

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
            raise AfterpayError("Cannot issue refund without an 'order_id'")
        if params is None:
            params = {}
        if "merchantReference" not in params and idempotency:
            raise AfterpayError("Cannot issue refund without 'merchantReference' while idempotency is enabled")
        if "amount" not in params:
            raise ParamsError("Cannot issue refund without an 'amount'")

        params.requestId = self.generate_uuid()

        return self.config.http().post(self.payments_url + "/" + order_id + "/refund/", params)

    def update(self, order_id=None, params=None):
        """
        This operation updates Afterpay with the merchant order ID after AfterPay order ID creation.
        This operation should be called immediately after the AfterPay order is created in order to
        properly update the order with the correct merchant order ID
        :param order_id: Order ID to update
        :param params: Request parameters
            merchantReference: The merchant’s new order ID
        """
        if order_id is None:
            raise AfterpayError("Cannot issue refund without an 'order_id'")
        if params is None:
            params = {}
        if "merchantReference" not in params:
            raise AfterpayError("Cannot update payment without 'merchantReference'")

        return self.config.http().put(self.payments_url + "/" + order_id, params)

    def update_courier(self, order_id=None, params=None):
        """
        This operation updates an order with shipping courier information.
        The Afterpay team may utilise this information when providing support.
        :param order_id: Order ID to update
        :param params: Request parameters
            shippedAt?: The date and time when the order was shipped, in ISO 8601 format.
            name?: The name of the shipping courier.
            tracking?: The shipping tracking number provided by the courier.
            priority?: The shipping priority. If provided, must be either "STANDARD" or "EXPRESS".
        """
        if order_id is None:
            raise AfterpayError("Cannot issue refund without an 'order_id'")
        if params is None:
            params = {}
        if "priority" not in ["STANDARD", "EXPRESS"]:
            raise AfterpayError("Courier update 'priority' must be either STANDARD or EXPRESS")

        return self.config.http().put(self.payments_url + "/" + order_id + "/courier/", params)

    def reverse(self, token=None):
        """
        This operation performs a reversal of the checkout that is used to initiate the Afterpay payment process.
        This will cancel the order asynchronously as soon as it is created without the need of an additional call
        to the void endpoint. In order for a payment to be eligible, the order must be in an Auth-Approved or
        Captured state and must be issued within 10 minutes of the order being created.
        :param token: Token of order to reverse
        :param params: Request parameters
            merchantReference: The merchant’s new order ID
        """
        if token is None:
            raise AfterpayError("Cannot issue reversal without a 'token'")

        return self.config.http().post(self.payments_url + "/token:" + token + "/reversal/")
