import json

from entities.person import Person
from entities.account import Account
from utilities.utils import TRANSACTION_FAILURE


class CustomerAccount(Person, Account):
    def __init__(self, first_name, last_name, address, account_type, account_no, balance):
        Person.__init__(self, first_name, last_name, address)
        Account.__init__(self, account_type, account_no, balance)

    def account_menu(self):
        print("\n Your Transaction Options Are:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) Deposit money")
        print("2) Withdraw money")
        print("3) Check balance")
        print("4) Update customer name")
        print("5) Update customer address")
        print("6) Show customer details")
        print("7) Back")
        print(" ")
        option = int(input("Choose your option: "))
        return option

    def print_details(self):
        print(self.get_details())

    def get_details(self):
        details = ""
        details += self.get_person_as_str()
        details += 'Account type: %s\n' % self.get_account_type()
        details += 'Account number: %s\n' % self.get_account_no()
        details += 'Balance: %.2f\n' % self.get_balance()
        details += 'Overdraft limit: %.2f\n' % self.get_overdraft_limit()
        details += 'Interest rate: %.2f\n' % self.get_interest_rate()
        return details

    def run_account_options(self):
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                amount = float(input('\n Please enter amount to be deposited: \n'))
                self.deposit(amount)
                self.print_balance()
            elif choice == 2:
                amount = float(input('\n Please enter amount to be withdrawn: \n'))
                state, msg = self.withdraw(amount)
                if state == TRANSACTION_FAILURE:
                    print('\n ' + msg + ' \n')
                    return
                self.print_balance()
            elif choice == 3:
                self.print_balance()
            elif choice == 4:
                first_name = input('\n Enter new customer first name: \n')
                last_name = input('\n Enter new customer last name: \n')
                self.update_first_name(first_name)
                self.update_last_name(last_name)
            elif choice == 5:
                street_num = input('\n Enter your current street number: \n')
                street_name = input('\n Enter your current street name: \n')
                city = input('\n Enter your city of residence: \n')
                postcode = input('\n Enter your postcode: \n')
                self.update_address(street_num, street_name, city, postcode)
                self.print_details()
            elif choice == 6:
                self.print_details()
            elif choice == 7:
                loop = 0
        print("\n Exit account operations")

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)


def load(data):
    return CustomerAccount(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=[data['street_number'], data['street_name'], data['city'], data['postcode']],
            account_type=data['account_type'],
            account_no=data['account_number'],
            balance=data['balance'],
        )
