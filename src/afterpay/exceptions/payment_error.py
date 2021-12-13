from afterpay.exceptions.afterpay_error import AfterpayError

class PaymentError(AfterpayError):
    """
    The Consumer has not confirmed their payment for the order associated with this token, or;
    Payment was declined by Afterpay
    """
    pass
