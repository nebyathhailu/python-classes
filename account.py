from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type, narration):
        self.date = datetime.now()
        self.amount = amount
        self.transaction_type = transaction_type
        self.narration = narration

    def __repr__(self):
        return f"{self.date} | {self.transaction_type} | {self.amount} | {self.narration}"
    
class Account:
    def __init__(self, name):
        self.name = name
        self.__account_balance = 0
        self.__loan_balance = 0
        self.is_frozen = False
        self.transactions = []
        self.loan_transactions = []
        self.min_balance = 100

    
    def __add_transaction(self, amount, transaction_type, narration=""):
        transaction = Transaction(amount, transaction_type, narration)
        self.transactions.append(transaction)

    def get_balance(self):
        for transaction in self.transactions:
            if transaction.transaction_type in ["Deposit", "Loan Received", "Transfer In"]:
                self.__account_balance += transaction.amount
            elif transaction.transaction_type in ["Withdraw", "Transfer Out", "Loan Repayment"]:
                self.__account_balance -= transaction.amount
        return f"Your balance is {self.__account_balance}."
    
    def deposit(self, amount):
        if self.is_frozen:
            return "Deposit failed: your account is frozen."
        if amount <= 0:
            return "Deposit must be positive."
        self.__add_transaction(amount, "Deposit")
        return self.get_balance()
    
    def withdraw(self, amount):
        if self.is_frozen:
            return "Withdrawal failed: your account is frozen."
        if amount <= 0:
            return "Enter a positive amount."
        if self.__account_balance - amount < self.min_balance:
            return f"Withdrawal failed: must maintain at least {self.min_balance} balance."
        self.__add_transaction(amount, "Withdraw")
        return self.get_balance()
    
    def transfer(self, amount, target_account):
        if self.is_frozen:
            return "Withdrawal failed: your account is frozen."
        if amount <= 0:
            return "Enter a positive amount."
        if self.__account_balance - amount < self.min_balance:
            return f"Transfer failed: must maintain at least {self.min_balance} balance."
        if isinstance(target_account, Account):
            self.__add_transaction(amount, "Transfer Out", f"To {target_account.name}")
            target_account.__add_transaction(amount, "Transfer In" , "From {self.name}")
            return self.get_balance()
        else:
            return "Target account doesn't exist."
        
    def get_loan(self, amount):
        if self.is_frozen:
            return "Loan request failed: your account is frozen."
        if amount <= 0:
            return "Loan amount must be positive."
        max_loan = 3 * self.__account_balance
        if amount > max_loan:
            return f"Loan request exceeds limit of {max_loan}."
        self.__add_transaction(amount, "Loan Received")
        self.__loan_transactions.append(Transaction(amount, "Loan Received"))
        self.__loan_balance += amount
        return f"Loan approved. Your new balance is {self.get_balance()}."
    
    def repay_loan(self, amount):
        if amount <= 0:
            return "Enter a positive amount."
        if self.__loan_balance == 0:
            return "No outstanding loan to repay."
        if self.__account_balance - amount < self.min_balance:
            return "Loan repayment failed: must maintain {self.min_balance} in account."
        self.__add_transaction(amount, "Loan Repayment")
        self.__loan_transactions.append(Transaction(amount, "Loan Repayment"))
        self.__loan_balance -= amount
        return f"Loan repaid. Remaining loan balance: {self.__loan_balance}"
    
    def get_loan_balance(self):
        for loan in self.loan_transactions:
            if loan.transaction_type == "Loan Received":
                self.__loan_balance += loan.amount
            elif loan.transaction_type ==  "Loan Repayment":
                self.__loan_balance -= loan.amount
        return f"You loan balance is {self.__loan_balance}."
    
    def get_loan_statement(self):
        return [str(txn) for txn in self.transactions]
    
    def show_balance(self):
        return f"Current balance: {self.get_balance()}"
    