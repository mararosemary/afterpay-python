from afterpay.exceptions.afterpay_error import AfterpayError

class InvalidHeadersError(AfterpayError):
    """
    The request included an Accept header for something other than application/json or */*, or;
    The request did not include a Content-Type header, or its value was anything other than application/json.
    """
    pass
