from afterpay.exceptions.afterpay_error import AfterpayError

class InvalidRequestError(AfterpayError):
    """
    The request body contains invalid or improperly formatted JSON.
    """
    pass
