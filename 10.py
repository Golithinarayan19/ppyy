class BankAccount:
    """
    Base class representing a generic bank account
    """

    def __init__(self, account_holder, account_number, balance=0):
        # Encapsulation: protected attributes
        self._account_holder = account_holder
        self._account_number = account_number
        self._balance = balance
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited ₹{amount}. New balance: ₹{self._balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            print(f"Withdrawn ₹{amount}. Remaining balance: ₹{self._balance}")
        else:
            print("Insufficient balance")
    def get_balance(self):
        return self._balance
    def display_details(self):
        print("Account Holder:", self._account_holder)
        print("Account Number:", self._account_number)
        print("Balance: ₹", self._balance)
class SavingsAccount(BankAccount):
    """
    Child class representing a savings account
    """

    def __init__(self, account_holder, account_number, balance=0, interest_rate=0.04):
        super().__init__(account_holder, account_number, balance)
        self.interest_rate = interest_rate
    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"Interest added: ₹{interest}. New balance: ₹{self._balance}")
class CurrentAccount(BankAccount):
    """
    Child class representing a current account
    """

    def withdraw(self, amount):
        # Overriding withdraw method
        if amount <= self._balance:
            self._balance -= amount
            print(f"Withdrawn ₹{amount} from Current Account")
        else:
            print("Overdraft not allowed in Current Account")
if __name__ == "__main__":
    # Object 1: Savings Account
    acc1 = SavingsAccount("Narayan", "SB1001", 5000)
    acc1.display_details()
    acc1.deposit(2000)
    acc1.add_interest()
    acc1.withdraw(1000)

    print("\n-------------------\n")

    # Object 2: Current Account
    acc2 = CurrentAccount("Anjali", "CA2001", 10000)
    acc2.display_details()
    acc2.deposit(5000)
    acc2.withdraw(3000)
    acc2.withdraw(20000)  # should fail
