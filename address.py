import json


class Address:

    def __init__(self, street_number, street_name, city, postcode):
        self.street_number = street_number
        self.street_name = street_name
        self.city = city
        self.postcode = postcode

    def get_address(self):
        return [self.street_number, self.street_name, self.city, self.postcode]

    def update_address(self, street_number, street_name, city, postcode):
        self.street_number = street_number
        self.street_name = street_name
        self.city = city
        self.postcode = postcode

    def print_address(self):
        print(self.get_address())

    def get_address_as_str(self):
        address = ""
        address += 'Address: %s\n' % self.street_number
        address += '       : %s\n' % self.street_name
        address += '       : %s\n' % self.city
        address += '       : %s\n' % self.postcode
        address += '\n'
        return address
