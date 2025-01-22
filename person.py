from entities.address import Address


class Person(Address):

    def __init__(self, first_name, last_name, address):
        Address.__init__(self, address[0], address[1], address[2], address[3])
        self.first_name = first_name
        self.last_name = last_name

    def get_first_name(self):
        return self.first_name

    def update_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def update_last_name(self, last_name):
        self.last_name = last_name

    def print_person(self):
        print(self.get_person_as_str())

    def get_person_as_str(self):
        person = ""
        person += 'First name: %s\n' % self.get_first_name()
        person += 'Last name: %s\n' % self.get_last_name()
        person += self.get_address_as_str()
        return person
