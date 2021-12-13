from afterpay.exceptions.afterpay_error import AfterpayError

class ParamsError(AfterpayError):
    """
    One or more required fields were missing or invalid, or;
    The amount is outside of the merchant's payment limits, as returned by Get Configuration, or;
    One or more Money objects may have contained a currency that differs from the merchant's account currency, or;
    The checkout token was missing or empty.
    """
    pass
