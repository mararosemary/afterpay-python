from afterpay.exceptions.afterpay_error import AfterpayError

class PaymentError(AfterpayError):
    """
    The Consumer has not confirmed their payment for the order associated with this token, or;
    Payment was declined by Afterpay, or;
    Payment not eligible for a reversal, or;
    Payment reversal previously processed, or;
    Order outside reversal window, or;
    Order in pending reversal, no captures/auth accepted
    """
    pass
