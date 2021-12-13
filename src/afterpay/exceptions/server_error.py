from afterpay.exceptions.afterpay_error import AfterpayError

class ServerError(AfterpayError):
    """
    A common cause of this response from PUT/POST endpoints is that the request body is missing or empty.
    """
    pass
