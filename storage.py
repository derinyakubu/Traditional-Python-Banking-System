import json

CUSTOMER_DB = "db/customer.json"
ADMIN_DB = "db/admin.json"


# CUSTOMER DB METHODS
def update_customer_accounts_db(updated_accounts):
    with open(CUSTOMER_DB, 'w') as f:
        f.write(json.dumps(updated_accounts, default=lambda o: o.__dict__, indent=4, sort_keys=True))
    return updated_accounts


# ADMIN DB METHODS
def update_admins_db(updated_admins):
    with open(ADMIN_DB, 'w') as f:
        f.write(json.dumps(updated_admins, default=lambda o: o.__dict__, indent=4, sort_keys=True))
    return updated_admins
