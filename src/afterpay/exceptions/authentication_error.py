from afterpay.exceptions.afterpay_error import AfterpayError

class AuthenticationError(AfterpayError):
    """
    Invalid Merchant API credentials were passed in the Authorization header.
    """
    pass
