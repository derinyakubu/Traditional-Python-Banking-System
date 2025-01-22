from utilities.utils import TRANSACTION_FAILURE, TRANSACTION_SUCCESS


CURRENT_ACCOUNT_TYPE = 'current'
SAVINGS_ACCOUNT_TYPE = 'savings'
CHECKING_ACCOUNT_TYPE = 'checking'
STUDENT_ACCOUNT_TYPE = 'student'


def get_account_details(account_type):
    if account_type == CURRENT_ACCOUNT_TYPE:
        return 0.75, 5000
    if account_type == CHECKING_ACCOUNT_TYPE:
        return 0.5, 4000
    if account_type == SAVINGS_ACCOUNT_TYPE:
        return 4.35, 3000
    if account_type == STUDENT_ACCOUNT_TYPE:
        return 1.25, 1000
    return 0, 0


class Account:

    def __init__(self, account_type, account_number, balance):
        interest_rate, overdraft_limit = get_account_details(account_type)
        self.account_type = account_type
        self.account_number = account_number
        self.interest_rate = interest_rate
        self.overdraft_limit = overdraft_limit
        self.balance = float(balance)

    def deposit(self, amount):
        if amount < 0:
            return TRANSACTION_FAILURE
        self.balance += amount
        return TRANSACTION_SUCCESS

    def withdraw(self, amount):
        if amount <= 1:
            print('\n You cannot withdraw negative or zero amounts')
            return TRANSACTION_FAILURE, "You cannot withdraw negative or zero amounts"
        if self.balance + self.overdraft_limit < amount:
            print('\n This customer does not have sufficient balance! \n')
            return TRANSACTION_FAILURE, "This customer does not have sufficient balance!"
        self.balance -= amount
        return TRANSACTION_SUCCESS, ""

    def print_balance(self):
        print("\n The account balance is %.2f" % self.balance)

    def get_balance(self):
        return self.balance

    def get_account_no(self):
        return self.account_number

    def get_account_type(self):
        return self.account_type

    def get_overdraft_limit(self):
        return self.overdraft_limit

    def get_interest_rate(self):
        return self.interest_rate
