from afterpay.exceptions.afterpay_error import AfterpayError

class TokenError(AfterpayError):
    """
    The checkout token is invalid, expired, or does not exist.
    """
    pass
