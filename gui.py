import tkinter
from bank_system import BankSystem
from entities.customer_account import CustomerAccount
from db.storage import update_admins_db, update_customer_accounts_db
from utilities.utils import TRANSACTION_FAILURE


class BankGUI(BankSystem):

    def __init__(self):
        BankSystem.__init__(self)
        self.win = None
        self.frame = None

    def run_gui(self):
        self.frame = None
        self.win = tkinter.Tk()
        self.win.title("Bank System")

        quit_button = tkinter.Button(self.win, text="Quit", command=self.quit)
        quit_button.grid(row=6, column=1)

        self.show_login_screen()

        tkinter.mainloop()

    def show_login_screen(self):
        self.frame = tkinter.Frame(master=self.win)

        welcome_msg = tkinter.Label(master=self.frame, text="Welcome to the Python Bank System")
        welcome_msg.grid(row=2, column=0)

        admin_username_label = tkinter.Label(master=self.frame, text="Username: ")
        admin_username_label.grid(row=3, column=0)
        admin_username_text = tkinter.Entry(master=self.frame, width=10)
        admin_username_text.grid(row=3, column=1)

        admin_password_label = tkinter.Label(master=self.frame, text="Password: ")
        admin_password_label.grid(row=4, column=0)
        admin_password_text = tkinter.Entry(master=self.frame, width=10)
        admin_password_text.grid(row=4, column=1)

        admin_login_button = tkinter.Button(master=self.frame, text="Login",
                                            command=lambda: self.admin_options(admin_username_text,
                                                                               admin_password_text))
        admin_login_button.grid(row=5, column=1)

        self.frame.grid(row=3, column=0, padx=10)

    def admin_options(self, username_entry, password_entry):
        msg, admin_obj = self.admin_login(username_entry.get(), password_entry.get())
        print(msg)
        if admin_obj is None:
            error_label = tkinter.Label(master=self.frame, text="Invalid username or password!", foreground="red")
            error_label.grid(row=6, column=0)
            return

        self.reset_frame()

        self.frame = tkinter.Frame(master=self.win)

        msg = 'Welcome %s %s. Please pick an option' % (admin_obj.get_first_name(), admin_obj.get_last_name())
        option_msg = tkinter.Label(master=self.frame, text=msg)
        option_msg.grid(row=2, column=0)

        chosen_option = tkinter.IntVar()
        transfer_money_option = tkinter.Radiobutton(self.frame, text='Transfer money', variable=chosen_option, value=1)
        customer_account_profile_option = tkinter.Radiobutton(self.frame,
                                                              text='Customer account operations & profile settings',
                                                              variable=chosen_option, value=2)
        delete_customer_option = tkinter.Radiobutton(self.frame, text='Delete customer', variable=chosen_option,
                                                     value=3)
        print_all_customers_option = tkinter.Radiobutton(self.frame, text='Print all customers detail',
                                                         variable=chosen_option, value=4)
        update_admin_name_option = tkinter.Radiobutton(self.frame, text='Update your name', variable=chosen_option,
                                                       value=5)
        update_admin_address_option = tkinter.Radiobutton(self.frame, text='Update your address',
                                                          variable=chosen_option, value=6)
        request_management_option = tkinter.Radiobutton(self.frame, text='Request management report',
                                                        variable=chosen_option, value=7)
        sign_out_option = tkinter.Radiobutton(self.frame, text='Sign out', variable=chosen_option, value=8)

        transfer_money_option.grid(row=3, column=0)
        customer_account_profile_option.grid(row=4, column=0)
        delete_customer_option.grid(row=5, column=0)
        print_all_customers_option.grid(row=6, column=0)
        update_admin_name_option.grid(row=7, column=0)
        update_admin_address_option.grid(row=8, column=0)
        request_management_option.grid(row=9, column=0)
        sign_out_option.grid(row=10, column=0)

        submit_button = tkinter.Button(master=self.frame, text="Submit",
                                       command=lambda: self.handle_admin_options(admin_obj, chosen_option))
        submit_button.grid(row=12, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def handle_admin_options(self, admin_obj, option):
        val = option.get()
        if val == 1:
            self.show_transfer_money_screen()
        elif val == 2:
            self.show_customer_account_profile_screen()
        elif val == 3:
            self.show_delete_customer_screen(admin_obj)
        elif val == 4:
            self.show_all_customer_details_screen()
        elif val == 5:
            self.show_update_name_screen("admin", admin_obj)
        elif val == 6:
            self.show_update_address_screen("admin", admin_obj)
        elif val == 7:
            self.request_management_report_screen()
        else:
            self.quit()

    def show_transfer_money_screen(self):
        self.reset_frame()

        self.frame = tkinter.Frame(master=self.win)

        amount_label = tkinter.Label(master=self.frame, text="Amount: ")
        amount_label.grid(row=2, column=0)
        amount_entry = tkinter.Entry(master=self.frame, width=10)
        amount_entry.grid(row=2, column=1)

        sender_last_name_label = tkinter.Label(master=self.frame, text="Sender Last Name: ")
        sender_last_name_label.grid(row=3, column=0)
        sender_last_name_entry = tkinter.Entry(master=self.frame, width=10)
        sender_last_name_entry.grid(row=3, column=1)

        sender_account_number_label = tkinter.Label(master=self.frame, text="Sender Account Number: ")
        sender_account_number_label.grid(row=4, column=0)
        sender_account_number_entry = tkinter.Entry(master=self.frame, width=10)
        sender_account_number_entry.grid(row=4, column=1)

        receiver_last_name_label = tkinter.Label(master=self.frame, text="Receiver Last Name: ")
        receiver_last_name_label.grid(row=5, column=0)
        receiver_last_name_entry = tkinter.Entry(master=self.frame, width=10)
        receiver_last_name_entry.grid(row=5, column=1)

        receiver_account_number_label = tkinter.Label(master=self.frame, text="Receiver Account Number: ")
        receiver_account_number_label.grid(row=6, column=0)
        receiver_account_number_entry = tkinter.Entry(master=self.frame, width=10)
        receiver_account_number_entry.grid(row=6, column=1)

        transfer_button = tkinter.Button(master=self.frame, text="Transfer Money",
                                         command=lambda: self.handle_transfer_money(amount_entry,
                                                                                    sender_last_name_entry,
                                                                                    sender_account_number_entry,
                                                                                    receiver_last_name_entry,
                                                                                    receiver_account_number_entry))
        transfer_button.grid(row=8, column=0)
        self.frame.grid(row=3, column=0, padx=10)

    def show_customer_account_profile_screen(self):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        surname_label = tkinter.Label(master=self.frame, text="Surname: ")
        surname_label.grid(row=2, column=0)
        surname_entry = tkinter.Entry(master=self.frame, width=10)
        surname_entry.grid(row=2, column=1)

        submit_button = tkinter.Button(master=self.frame, text="Submit",
                                       command=lambda: self.run_customer_account_options(surname_entry))
        submit_button.grid(row=4, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def show_delete_customer_screen(self, admin_obj):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        account_num_label = tkinter.Label(master=self.frame, text="Account Number: ")
        account_num_label.grid(row=2, column=0)
        account_num_entry = tkinter.Entry(master=self.frame, width=10)
        account_num_entry.grid(row=2, column=1)

        submit_button = tkinter.Button(master=self.frame, text="Submit",
                                       command=lambda: self.handle_delete_customer(admin_obj, account_num_entry))
        submit_button.grid(row=4, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def handle_delete_customer(self, admin_obj, account_num_entry):
        customer_obj = self.delete_customer_account(admin_obj, account_num_entry.get())
        if customer_obj is None:
            error_label = tkinter.Label(master=self.frame, text="Customer account to delete does not exist", foreground="red")
            error_label.grid(row=6, column=0)
            self.frame.grid(row=3, column=0, padx=10)
            return

        self.show_user_details(customer_obj)

    def show_all_customer_details_screen(self):
        details = self.get_all_accounts_details()

        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        textarea = tkinter.Text(master=self.frame, height=20, width=30)
        textarea.pack()
        textarea.insert(tkinter.END, details)

        self.frame.grid(row=3, column=0, padx=10)

    def show_update_name_screen(self, user, user_obj):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        first_name_label = tkinter.Label(master=self.frame, text="First name: ")
        first_name_label.grid(row=3, column=0)
        first_name_entry = tkinter.Entry(master=self.frame, width=10)
        first_name_entry.grid(row=3, column=1)

        last_name_label = tkinter.Label(master=self.frame, text="Last name: ")
        last_name_label.grid(row=4, column=0)
        last_name_entry = tkinter.Entry(master=self.frame, width=10)
        last_name_entry.grid(row=4, column=1)

        if user == "admin":
            update_button = tkinter.Button(master=self.frame, text="Update",
                                           command=lambda: self.handle_update_admin_name(user_obj, first_name_entry,
                                                                                         last_name_entry))
        else:
            update_button = tkinter.Button(master=self.frame, text="Update",
                                           command=lambda: self.handle_update_customer_name(user_obj, first_name_entry,
                                                                                            last_name_entry))

        update_button.grid(row=5, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def handle_update_admin_name(self, admin_obj, first_name_entry, last_name_entry):
        admin_obj.update_first_name(first_name_entry.get())
        admin_obj.update_last_name(last_name_entry.get())

        updated_admins = []
        for adm in self.get_admins():
            if adm.get_username() != admin_obj.get_username():
                updated_admins.append(adm)
        updated_admins.append(admin_obj)

        self.set_admins(update_admins_db(updated_admins))
        self.show_user_details(admin_obj)

    def handle_update_customer_name(self, customer_obj, first_name_entry, last_name_entry):
        customer_obj.update_first_name(first_name_entry.get())
        customer_obj.update_last_name(last_name_entry.get())

        updated_accounts = []
        for customer_acc in self.get_customer_accounts():
            if customer_acc.get_account_no() != customer_obj.get_account_no():
                updated_accounts.append(customer_acc)
        updated_accounts.append(customer_obj)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        self.show_user_details(customer_obj)

    def show_update_address_screen(self, user, user_obj):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        street_number_label = tkinter.Label(master=self.frame, text="Street number: ")
        street_number_label.grid(row=3, column=0)
        street_number_entry = tkinter.Entry(master=self.frame, width=10)
        street_number_entry.grid(row=3, column=1)

        street_name_label = tkinter.Label(master=self.frame, text="Street name: ")
        street_name_label.grid(row=4, column=0)
        street_name_entry = tkinter.Entry(master=self.frame, width=10)
        street_name_entry.grid(row=4, column=1)

        city_label = tkinter.Label(master=self.frame, text="City: ")
        city_label.grid(row=5, column=0)
        city_entry = tkinter.Entry(master=self.frame, width=10)
        city_entry.grid(row=5, column=1)

        postcode_label = tkinter.Label(master=self.frame, text="Postcode: ")
        postcode_label.grid(row=6, column=0)
        postcode_entry = tkinter.Entry(master=self.frame, width=10)
        postcode_entry.grid(row=6, column=1)

        if user == "admin":
            update_button = tkinter.Button(master=self.frame, text="Update",
                                           command=lambda: self.handle_update_admin_address(user_obj,
                                                                                            street_number_entry,
                                                                                            street_name_entry,
                                                                                            city_entry,
                                                                                            postcode_entry))
        else:
            update_button = tkinter.Button(master=self.frame, text="Update",
                                           command=lambda: self.handle_update_customer_address(user_obj,
                                                                                               street_number_entry,
                                                                                               street_name_entry,
                                                                                               city_entry,
                                                                                               postcode_entry))

        update_button.grid(row=7, column=0)
        self.frame.grid(row=3, column=0, padx=10)

    def handle_update_admin_address(self, admin_obj, street_number_entry, street_name_entry, city_entry,
                                    postcode_entry):
        admin_obj.update_address(street_number_entry.get(), street_name_entry.get(), city_entry.get(),
                                 postcode_entry.get())

        updated_admins = []
        for adm in self.get_admins():
            if adm.get_username() != admin_obj.get_username():
                updated_admins.append(adm)
        updated_admins.append(admin_obj)

        self.set_admins(update_admins_db(updated_admins))
        self.show_user_details(admin_obj)

    def handle_update_customer_address(self, customer_obj, street_number_entry, street_name_entry,
                                       city_entry,
                                       postcode_entry):
        customer_obj.update_address(street_number_entry.get(), street_name_entry.get(), city_entry.get(),
                                    postcode_entry.get())

        updated_accounts = []
        for customer_acc in self.get_customer_accounts():
            if customer_acc.get_account_no() != customer_obj.get_account_no():
                updated_accounts.append(customer_acc)
        updated_accounts.append(customer_obj)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        self.show_user_details(customer_obj)

    def request_management_report_screen(self):
        report = self.request_report()

        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        textarea = tkinter.Text(master=self.frame, height=20, width=30)
        textarea.pack()
        textarea.insert(tkinter.END, report)

        self.frame.grid(row=3, column=0, padx=10)

    def run_customer_account_options(self, customer_name):
        customer_obj = self.search_customers_by_last_name(customer_name.get())
        if customer_obj is None:
            error_label = tkinter.Label(master=self.frame, text="Customer does not exist!", foreground="red")
            error_label.grid(row=6, column=0)
            return

        self.reset_frame()

        self.frame = tkinter.Frame(master=self.win)

        msg = 'Welcome to %s %s\'s account. Please pick an option' % (customer_obj.get_first_name(), customer_obj.get_last_name())
        option_msg = tkinter.Label(master=self.frame, text=msg)
        option_msg.grid(row=2, column=0)

        chosen_option = tkinter.IntVar()
        deposit_money_option = tkinter.Radiobutton(self.frame, text='Deposit money', variable=chosen_option, value=1)
        withdraw_money_option = tkinter.Radiobutton(self.frame, text='Withdraw money', variable=chosen_option, value=2)
        check_balance_option = tkinter.Radiobutton(self.frame, text='Check balance', variable=chosen_option, value=3)
        update_customer_name_option = tkinter.Radiobutton(self.frame, text='Update customer name',
                                                          variable=chosen_option, value=4)
        update_customer_address_option = tkinter.Radiobutton(self.frame, text='Update customer address',
                                                             variable=chosen_option,
                                                             value=5)
        show_customer_option = tkinter.Radiobutton(self.frame, text='Show customer details',
                                                   variable=chosen_option, value=6)

        deposit_money_option.grid(row=3, column=0)
        withdraw_money_option.grid(row=4, column=0)
        check_balance_option.grid(row=5, column=0)
        update_customer_name_option.grid(row=6, column=0)
        update_customer_address_option.grid(row=7, column=0)
        show_customer_option.grid(row=8, column=0)

        submit_button = tkinter.Button(master=self.frame, text="Submit",
                                       command=lambda: self.handle_customer_options(chosen_option, customer_obj))
        submit_button.grid(row=12, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def handle_customer_options(self, option, customer_obj):
        val = option.get()
        if val == 1:
            self.show_deposit_money_screen(customer_obj)
        elif val == 2:
            self.show_withdraw_money_screen(customer_obj)
        elif val == 3:
            self.handle_check_balance(customer_obj)
        elif val == 4:
            self.show_update_name_screen("customer", customer_obj)
        elif val == 5:
            self.show_update_address_screen("customer", customer_obj)
        elif val == 6:
            self.show_user_details(customer_obj)
        else:
            self.quit()

    def handle_transfer_money(self, amount_entry, sender_last_name_entry, sender_account_number_entry,
                              receiver_last_name_entry,
                              receiver_account_number_entry):
        sender_last_name = sender_last_name_entry.get()
        sender_account_no = sender_account_number_entry.get()
        receiver_last_name = receiver_last_name_entry.get()
        receiver_account_no = receiver_account_number_entry.get()
        amount = amount_entry.get()

        result, err_msg = self.transfer_money(amount, sender_last_name, sender_account_no, receiver_last_name,
                                              receiver_account_no)
        if result == TRANSACTION_FAILURE:
            error_label = tkinter.Label(master=self.frame, text=err_msg, foreground="red")
            error_label.grid(row=9, column=0)
            self.frame.grid(row=3, column=0, padx=10)
            return

        self.show_all_customer_details_screen()

    def handle_deposit(self, customer_obj, amount_entry):
        amount = float(amount_entry.get())
        if customer_obj.deposit(amount) == TRANSACTION_FAILURE:
            error_label = tkinter.Label(master=self.frame, text="You cannot deposit negative money", foreground="red")
            error_label.grid(row=5, column=0)
            self.frame.grid(row=3, column=0, padx=10)
            return

        updated_accounts = []
        for customer_acc in self.get_customer_accounts():
            if customer_acc.get_account_no() != customer_obj.get_account_no():
                updated_accounts.append(customer_acc)
        updated_accounts.append(customer_obj)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        self.show_user_details(customer_obj)

    def handle_withdrawal(self, customer_obj, amount_entry):
        amount = float(amount_entry.get())
        state, msg = customer_obj.withdraw(amount)
        if state == TRANSACTION_FAILURE:
            error_label = tkinter.Label(master=self.frame, text=msg, foreground="red")
            error_label.grid(row=6, column=0)
            self.frame.grid(row=3, column=0, padx=10)
            return

        updated_accounts = []
        for customer_acc in self.get_customer_accounts():
            if customer_acc.get_account_no() != customer_obj.get_account_no():
                updated_accounts.append(customer_acc)
        updated_accounts.append(customer_obj)

        self.set_customer_accounts(update_customer_accounts_db(updated_accounts))
        self.show_user_details(customer_obj)

    def handle_check_balance(self, customer_obj: CustomerAccount):
        balance = customer_obj.get_balance()
        details = 'Account balance: %.2f' % balance

        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        textarea = tkinter.Text(master=self.frame, height=20, width=30)
        textarea.pack()
        textarea.insert(tkinter.END, details)

        self.frame.grid(row=3, column=0, padx=10)

    def show_user_details(self, user):
        details = user.get_details()

        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        textarea = tkinter.Text(master=self.frame, height=20, width=30)
        textarea.pack()
        textarea.insert(tkinter.END, details)

        self.frame.grid(row=3, column=0, padx=10)

    def reset_frame(self):
        self.frame.destroy()

    def quit(self):
        print("Quitting the Python Bank System")
        self.win.quit()

    def show_deposit_money_screen(self, customer_obj):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        amount_label = tkinter.Label(master=self.frame, text="Amount: ")
        amount_label.grid(row=2, column=0)
        amount_entry = tkinter.Entry(master=self.frame, width=10)
        amount_entry.grid(row=2, column=1)

        deposit_button = tkinter.Button(master=self.frame, text="Deposit",
                                        command=lambda: self.handle_deposit(customer_obj, amount_entry))
        deposit_button.grid(row=4, column=0)

        self.frame.grid(row=3, column=0, padx=10)

    def show_withdraw_money_screen(self, customer_obj):
        self.reset_frame()
        self.frame = tkinter.Frame(master=self.win)

        amount_label = tkinter.Label(master=self.frame, text="Amount: ")
        amount_label.grid(row=2, column=0)
        amount_entry = tkinter.Entry(master=self.frame, width=10)
        amount_entry.grid(row=2, column=1)

        withdraw_button = tkinter.Button(master=self.frame, text="Withdraw",
                                         command=lambda: self.handle_withdrawal(customer_obj, amount_entry))
        withdraw_button.grid(row=4, column=0)

        self.frame.grid(row=3, column=0, padx=10)


bank_app = BankGUI()

# By default, the gui is run. To run the console,
# comment 'bank_app.run_gui()' and uncomment 'bank_app.run_main_options()'
bank_app.run_gui()

# Uncomment the line below to run the console.
# Remember to comment out the 'bank_app.run_gui()' line
# bank_app.run_main_options()
