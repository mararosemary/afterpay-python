from afterpay.attribute_getter import AttributeGetter
from afterpay.exceptions import AfterpayError


class Consumer(AttributeGetter):
    """
    Consumer object
    Attributes:
        email: The consumer’s email address. Limited to 128 characters.
        phoneNumber?: The consumer’s phone number. Limited to 32 characters.
        givenNames?: The consumer’s first name and any middle names. Limited to 128 characters.
        surname?: The consumer’s last name. Limited to 128 characters.
    """
    attribute_list = [
        "email",
        "phoneNumber",
        "givenNames",
        "surname",
    ]

    def __init__(self, attributes):
        if "email" not in attributes:
            raise AfterpayError("Cannot initialize Consumer object without an 'email'")

        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(Consumer, self).__repr__(self.attribute_list)

    def get_json(self):
        return {
            i: super(Consumer, self).__dict__[i] for i in super(Consumer, self).__dict__ if i in self.attribute_list
        }
