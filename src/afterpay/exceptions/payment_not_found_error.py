from afterpay.exceptions.afterpay_error import AfterpayError

class PaymentNotFoundError(AfterpayError):
    """
    No Afterpay Order was found for retrieval request
    """
    pass