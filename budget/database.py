import sqlite3

class Database:

    def __init__(self, db_name):

        self.conn = sqlite3.connect(db_name)

        self.cursor = self.conn.cursor() 

    def add_transactions(self, values):
       # add code to prevent duplicates? 
        self.cursor.executemany(
            "INSERT INTO transactions (source_id, transaction_type, account_id, full_description, formatted_description, transaction_city, transaction_state, transaction_amount, record_date, transaction_date, account_number, bank_id, entered_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", values
        )

        self.conn.commit()

    def add_spendingAccounts(self, values):

        self.cursor.executemany(
            "INSERT INTO spending_accounts (account_id, account_name, account_type, account_sub_type) VALUES (?,?,?,?)", values
        )

    def add_bankAccounts(self, values):

        self.cursor.executemany(
            "INSERT INTO bank_accounts (account_number, bank_id, account_type) VALUES (?,?,?)", values
        )

    def add_budgets(self, values):
        self.cursor.executemany(
            "INSERT INTO budgets (budget_year, budget_month, account_id, budget_amount) VALUES (?,?,?,?)", values
        )

    def add_banks(self, values):
        self.cursor.executemany(
            "INSERT INTO banks (bank_id, bank_name, bank_type) VALUES (?,?,?)", values
        )
