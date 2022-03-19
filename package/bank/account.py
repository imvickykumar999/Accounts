
class Bank_Account:

    def __init__(self, balance = 0):
        self.balance = balance
        # print("Hello!!! Welcome to the Deposit & Withdrawal Machine")

    def deposit(self, amount):
        # amount=float(input("Enter amount to be Deposited: "))
        self.balance += amount
        # print("\n Amount Deposited:", amount)
        return self.balance

    def withdraw(self, amount):
        # amount = float(input("Enter amount to be Withdrawn: "))

        if self.balance>=amount:
            self.balance-=amount
            # print("\n You Withdraw:", amount)
            return self.balance
        else:
            # print("\n Insufficient balance ")
            return self.balance

    def display(self):
        # print("\n Net Available Balance=", self.balance)
        return self.balance
