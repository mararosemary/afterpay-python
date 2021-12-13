from afterpay.exceptions.afterpay_error import AfterpayError

class InvalidMethodError(AfterpayError):
    """
    The request was made using an unacceptable HTTP Method.
    Depending on the endpoint, only PUT or POST requests will be allowed.
    Use the OPTIONS HTTP Method to determine which methods are allowed for each endpoint.
    """
    pass
