class Account:
    def __init__(self, name):
        self.name = name
        self.account_balance = 0
        self.deposits = []
        self.withdraws = []
        self.transfers = []
        self.loans = []
        self.paid_loans = []
        self.loan_balance = 0
        self.is_frozen = False

    #Calculate total balance
    def get_balance(self, balance):
        total = 0
        for i in balance:
            total+=i
        return total

    #Set minimum Balance
    def set_min_balance(self):
        min_balance = 100
        return min_balance
    
    #Deposit
    def deposit(self, amount):
        if self.is_frozen == False:
            if amount > 0:
                self.deposits.append(amount)
                self.account_balance = self.get_balance(self.deposits) - self.get_balance(self.withdraws) - self.get_balance(self.transfers)
                return self.account_balance
            else:
                return "Deposit can't be negative."
        else:
            return "Deposit failed: your account is frozen."

    #Withdraw
    def withdraw(self, amount):
        if self.is_frozen == False:
            if amount > 0:
                if amount < self.account_balance:
                    if amount <= self.account_balance - self.set_min_balance():
                        self.withdraws.append(amount)
                        self.account_balance = self.get_balance(self.deposits) - self.get_balance(self.withdraws) - self.get_balance(self.transfers)
                        return self.account_balance
                    else:
                        return f"Withdrawal failed: you must keep at least {self.set_min_balance()} in your account."
                else:
                    return "Insufficient balance"
            else:
                return "Enter positive amount."
        else:
            return "Withdrawal fail: your account is frozen."
        
    #Transfer
    def transfer(self, amount, account):
        if self.is_frozen == False:
            if amount > 0:
                if amount <= self.account_balance - self.set_min_balance():
                    self.transfers.append(amount)
                    account.deposit(amount)
                    self.account_balance = self.get_balance(self.deposits) - self.get_balance(self.withdraws) - self.get_balance(self.transfers)
                    account.account_balance = account.get_balance(account.deposits) - account.get_balance(account.withdraws)
                    return self.account_balance
                else:
                    return f"Transfer failed: you must keep at least {self.set_min_balance()} in your account."
            else:
                return "Can't transfer negative amount."
        else:
            return "Transfer failed: your account is frozen."
        
    #Get loan
    def get_loan(self,amount):
        if amount > 0:
            max_loan = 3 * self.account_balance 
            if amount <= max_loan:
                self.loans.append(amount)
                self.deposit(amount)
                self.loan_balance = self.get_balance(self.loans) - self.get_balance(self.paid_loans)
                return self.loan_balance
            else:
                return f"You can't get a loan greater than {max_loan}."
        else:
            return "Loan amount can't be negative."
        
    #Repay loan
    def repay_loan(self, amount):
        if amount > 0:
            if self.loan_balance != 0:
                self.withdraw(amount)
                self.paid_loans.append(amount)
                self.loan_balance = self.get_balance(self.loans) - self.get_balance(self.paid_loans)
                return self.loan_balance
            else:
                return "You don't have any loans."
        else:
            return "Amount can't be negative."

    #Show balance  
    def show_balance(self):
        return f"Your balance is {self.account_balance}"
    
    #Account Statement
    def get_statement(self):
        statements =[{"type":"Deposit", "amount":self.get_balance(self.deposits)},
                    {"type":"Transfer", "amount":self.get_balance(self.transfers)},
                    {"type":"Withdraw", "amount":self.get_balance(self.withdraws)},
                    {"type":"Account balance", "amount":self.account_balance}]
        for statement in statements:
            return f"{statement["type"]}: {statement["amount"]}"

    #Get loan statement
    def get_loan_statement(self):
        statements = [{"type":"Loan taken", "amount":self.get_balance(self.loans)},
                      {"type":"Paid loan", "amount":self.paid_loans},
                      {"type":"Unpaid loan", "amount":self.loan_balance}]
        for statement in statements:
            return f"{statement["type"]}: {statement["amount"]}"
        
    #Change account owner
    def change_owner(self, new_name):
        self.name = new_name
        return self.name
        
    #Interest calculation - compound interest n--> number of compounding per year , time in years
    def interest(self, time):
        rate = 0.05
        n = 12   #monthly
        interest = self.account_balance * (1 + rate/n) ** (n * time) - self.account_balance
        self.account_balance = "{:.2f}".format(self.account_balance * (1 + rate/n) ** (n * time))
        return f"Your interest for {time} year is {interest:.2f}."
    
    #Account details
    def account_details(self):
        owner = {"name":self.name , "balance":self.account_balance}
        return owner
    
    #Close account
    def close_account(self):
        self.balance = 0
        self.deposits.clear()
        self.withdraws.clear()
        self.transfers.clear()

    #Freeze account
    def freeze_account(self):
        self.is_frozen = True

    #Unfreeze account
    def unfreeze_account(self):
        self.is_frozen = False
        

