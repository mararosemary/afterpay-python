from afterpay.attribute_getter import AttributeGetter
from afterpay.exceptions import AfterpayError


class Contact(AttributeGetter):
    """
    Contact object
    Attributes:
        name: Full name of contact. Limited to 255 characters
        line1: First line of the address. Limited to 128 characters
        line2?: Second line of the address. Limited to 128 characters.
        area1: AU: Suburb, NZ: Town or city, UK: Postal town, US: City, CA: City. Limited to 128 characters.
        area2: NZ: Suburb, UK: Village or local area. Limited to 128 characters.
        region: AU: State, NZ: Region, UK: County, US: State, CA: Province or Territory.
        Limited to 128 characters.
        postcode: ZIP or postal code. Limited to 128 characters.
        countryCode: The ISO 3166-1 country code. Limited to 2 characters.
        phoneNumber?: The phone number, in E.123 format. Limited to 32 characters.
    """
    attribute_list = [
        "name",
        "line1",
        "line2",
        "area1",
        "area2",
        "region",
        "postcode",
        "countryCode",
        "phoneNumber",
    ]

    def __init__(self, attributes):
        if "name" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'name'")
        if "line1" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'line1'")
        if "area1" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without an 'area1'")
        if "area2" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without an 'area2'")
        if "region" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'region'")
        if "postcode" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'postcode'")
        if "countryCode" not in attributes:
            raise AfterpayError("Cannot initialize Contact object without a 'countryCode'")

        AttributeGetter.__init__(self, attributes)

    def __repr__(self):
        return super(Contact, self).__repr__(self.attribute_list)

    def get_json(self):
        return {
            i: super(Contact, self).__dict__[i] for i in super(Contact, self).__dict__ if i in self.attribute_list
        }
