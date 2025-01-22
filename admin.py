import json
from entities.person import Person


class Admin(Person):

    def __init__(self, first_name, last_name, address, user_name, password, full_rights):
        Person.__init__(self, first_name, last_name, address)
        self.user_name = user_name
        self.password = password
        self.full_admin_rights = full_rights

    def get_username(self):
        return self.user_name

    def set_username(self, user_name):
        self.user_name = user_name

    def update_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def has_full_admin_right(self):
        return self.full_admin_rights

    def set_full_admin_right(self, admin_right):
        self.full_admin_rights = admin_right

    def print_details(self):
        print(self.get_details())

    def get_details(self):
        person = self.get_person_as_str()
        person += 'Full admin rights: %s\n' % self.has_full_admin_right()
        return person

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)


def load(data):
    return Admin(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=[data['street_number'], data['street_name'], data['city'], data['postcode']],
            user_name=data['user_name'],
            password=data['password'],
            full_rights=data['full_admin_rights'],
        )
