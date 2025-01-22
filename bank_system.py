import json
import os.path

from entities import admin, customer_account
from entities.customer_account import CustomerAccount
from entities.admin import Admin
from db.storage import update_customer_accounts_db, ADMIN_DB, CUSTOMER_DB
from utilities.utils import TRANSACTION_FAILURE, TRANSACTION_SUCCESS

accounts_list = []
admins_list = []


class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        self.load_bank_data()

    def load_data(self, db):
        if not os.path.isfile(db):
            print('\n Database file is missing! \n')
            return

        with open(db) as f:
            entities = json.load(f)

        if db == ADMIN_DB:
            for entity in entities:
                self.admins_list.append(admin.load(entity))
        elif db == CUSTOMER_DB:
            for entity in entities:
                self.accounts_list.append(customer_account.load(entity))

    def load_bank_data(self):
        print('\n Reading admin accounts from DB \n')
        self.load_data(ADMIN_DB)

        print('\n Reading customer accounts from DB \n')
        self.load_data(CUSTOMER_DB)

    def get_customer_accounts(self) -> [CustomerAccount]:
        return self.accounts_list

    def set_customer_accounts(self, accs_list):
        self.accounts_list = accs_list

    def get_admins(self) -> [Admin]:
        return self.admins_list

    def set_admins(self, adms_list):
        self.admins_list = adms_list

    def search_admins_by_username(self, username):
        for adm in self.admins_list:
            if username == adm.get_username():
                return adm
        print('\n The Admin with username: %s does not exist! Try again... /n' % username)
        return None

    def search_customers_by_last_name(self, customer_last_name):
        for customer in self.get_customer_accounts():
            if customer_last_name == customer.get_last_name():
                return customer
        print('\n The Customer with last name: %s does not exist! Try again... \n' % customer_last_name)
        return None

    def search_customers_by_account_number(self, account_number):
        account_number = int(account_number)
        for customer_acc in self.get_customer_accounts():
            if account_number == customer_acc.get_account_no():
                return customer_acc
        print('\n The account number does not exist. Try again! \n')
        return None

    def delete_customer_account(self, admin_obj, account_number):
        if not admin_obj.has_full_admin_right():
            print('\n You do not have the rights to close a customer account! \n')
            return None

        customer_account_to_delete = self.search_customers_by_account_number(account_number)
        if customer_account_to_delete is None:
            print('\n Failed to delete customer. Try again! \n')
            return None

        updated_accounts = []
        for account in self.get_customer_accounts():
            if customer_account_to_delete.get_account_no() != account.get_account_no():
                updated_accounts.append(account)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        return customer_account_to_delete

    def main_menu(self):
        # print the options you have
        print()
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Welcome to the Python Bank System")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) Admin login")
        print("2) Quit Python Bank System")
        print(" ")
        option = int(input("Choose your option: "))
        return option

    def run_main_options(self):
        loop = 1
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input("\n Please input admin username: ")
                password = input("\n Please input admin password: ")
                msg, admin_obj = self.admin_login(username, password)
                print(msg)
                if admin_obj != None:
                    self.run_admin_options(admin_obj)
            elif choice == 2:
                loop = 0

        print("\n Thank you for stopping by the bank!")

    def transfer_money(self, amount, sender_last_name, sender_account_no, receiver_last_name, receiver_account_no):
        sender = self.search_customers_by_account_number(sender_account_no)
        receiver = self.search_customers_by_account_number(receiver_account_no)
        err_msg = ""

        try:
            amount = float(amount)
        except ValueError:
            err_msg = "Transfer failed: Amount must be a numerical value"
            print(err_msg)
            return TRANSACTION_FAILURE, err_msg

        if sender is None:
            err_msg = "Transfer failed: sender does not exist"
        elif sender.get_last_name() != sender_last_name:
            err_msg = "Transfer failed: sender last name does not match the account number"
        elif receiver is None:
            err_msg = "Transfer failed: receiver does not exist"
        elif receiver.get_last_name() != receiver_last_name:
            err_msg = "Transfer failed: receiver last name does not match the account number"
        elif sender.withdraw(amount) == TRANSACTION_FAILURE:
            err_msg = "Transfer failed: sender does not have enough money to transfer"

        if err_msg != "":
            print(err_msg)
            return TRANSACTION_FAILURE, err_msg

        receiver.deposit(amount)

        updated_accounts = []
        for account in self.get_customer_accounts():
            if sender.get_account_no() != account.get_account_no() and receiver.get_account_no() != account.get_account_no():
                updated_accounts.append(account)
        updated_accounts.append(sender)
        updated_accounts.append(receiver)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        return TRANSACTION_SUCCESS, "Transfer successful"

    def request_report(self):
        number_of_customers = self.count_customer_accounts()
        total_balance = self.get_total_balance_of_customers()
        total_overdraft = self.get_total_overdraft_of_customers()
        total_interest = self.get_total_interest_rates()

        report = ""
        report += '\nNumber of customers: %d\n' % number_of_customers
        report += "Total balance: %d GBP\n" % total_balance
        report += "Total overdraft: %.2f GBP\n" % total_overdraft
        report += "Total interest: %.2f GBP\n" % total_interest

        return report

    def admin_login(self, username, password):
        found_admin = self.search_admins_by_username(username)
        msg = '\n Login Failed'
        if found_admin is None:
            return msg, None
        if found_admin.get_password() != password:
            return msg, None
        msg = '\n Login successful'
        return msg, found_admin

    def admin_menu(self, admin_obj):
        # print the options you have
        print(" ")
        print("Welcome Admin %s %s : Available options are:" % (admin_obj.get_first_name(), admin_obj.get_last_name()))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) Transfer money")
        print("2) Customer account operations & profile settings")
        print("3) Delete customer")
        print("4) Print all customers detail")
        print("5) Update your name")
        print("6) Update your address")
        print("7) Request management report")
        print("8) Sign out")
        print(" ")
        option = int(input("Choose your option: "))
        return option

    def run_admin_options(self, admin_obj: Admin):
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin_obj)
            if choice == 1:
                amount = input("\n Please input the amount to be transferred: ")
                sender_last_name = input("\n Please input sender surname: ")
                sender_account_no = input("\n Please input sender account number: ")
                receiver_last_name = input("\n Please input receiver surname: ")
                receiver_account_no = input("\n Please input receiver account number: ")
                result, err_msg = self.transfer_money(amount, sender_last_name, sender_account_no, receiver_last_name,
                                                      receiver_account_no)
                if result == TRANSACTION_FAILURE:
                    print(err_msg)

            elif choice == 2:
                customer_name = input('\n Please input customer surname: \n')
                customer_acc = self.search_customers_by_last_name(customer_name)
                if customer_acc is not None:
                    customer_acc.run_account_options()

            elif choice == 3:
                account_num = input('\n Enter the account number of customer to be deleted: \n')
                self.delete_customer_account(admin_obj, account_num)

            elif choice == 4:
                for customer_acc in self.get_customer_accounts():
                    customer_acc.print_details()

            elif choice == 5:
                first_name = input('\n Enter new first name: \n')
                last_name = input('\n Enter new last name: \n')
                admin_obj.update_first_name(first_name)
                admin_obj.update_last_name(last_name)
                print('\n Information updated: \n')
                admin_obj.print_person()

            elif choice == 6:
                street_num = input('\n Enter your current street number: \n')
                street_name = input('\n Enter your current street name: \n')
                city = input('\n Enter your city of residence: \n')
                postcode = input('\n Enter your postcode: \n')
                admin_obj.update_address(street_num, street_name, city, postcode)
                print('\n Information updated: \n')
                admin_obj.print_person()

            elif choice == 7:
                print(self.request_report())

            elif choice == 8:
                loop = 0
        print("\n Exit account operations")

    def print_all_accounts_details(self):
        # list related operation - move to main.py
        print(self.get_all_accounts_details())

    def get_all_accounts_details(self):
        details = ""
        i = 0
        for c in self.get_customer_accounts():
            i += 1
            details += '\n %d.  ' % i
            details += c.get_details()
            details += "------------------------\n"
        return details

    def print_all_admin_details(self):
        # list related operation - move to main.py
        i = 0
        for c in self.admins_list:
            i += 1
            print('\n %d. ' % i, end=' ')
            c.print_details()
            print("------------------------")

    def count_customer_accounts(self):
        # TODO: should return the number of customers, not accounts
        return len(self.get_customer_accounts())

    def get_total_balance_of_customers(self):
        total_balance = 0
        for account in self.get_customer_accounts():
            total_balance += account.get_balance()
        return total_balance

    def get_total_overdraft_of_customers(self):
        total_overdraft = 0
        for account in self.get_customer_accounts():
            account_balance = account.get_balance()
            if account_balance < 0:
                total_overdraft += abs(account_balance)
        return total_overdraft

    def get_total_interest_rates(self):
        total_interest = 0
        for account in self.get_customer_accounts():
            principal_amount = account.get_balance()
            interest_rate = account.get_interest_rate()
            total_interest += principal_amount * (interest_rate / 100) * 1
        return total_interest
