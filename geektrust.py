import math
import sys
from collections import defaultdict

import enum

class Actions(enum.Enum):
    # valid commands
    payment = "PAYMENT"
    loan = "LOAN"
    balance = "BALANCE"


class Bank:

    def __init__(self, name):
        self.name = name
        # only one loan per borrower
        self.loans = {}

    def loan(self, borrower_name, principal, years, rate):
        l = Loan(principal, years, rate)
        self.loans[borrower_name] = l

    def payment(self, borrower_name, lump_sum, emi_num):
        self.loans[borrower_name].payment(lump_sum, emi_num)

    def balance(self, borrower_name, emi_num):
        paid_amount, emi_rem = self.loans[borrower_name].balance(emi_num)
        print(f"{self.name} {borrower_name} {int(paid_amount)} {int(emi_rem)}")


class Loan:
    def __init__(self, p, n, r):
        self.principal = float(p)
        self.time = float(n)
        self.rate = float(r) / 100
        self.total_interest = math.ceil(self.principal * self.time * self.rate)
        self.repay_amount = math.ceil(self.principal + self.total_interest)
        self.emi_count = math.ceil(self.time * 12)
        self.monthly_emi = math.ceil(self.repay_amount / self.emi_count)
        self.txn_log = {}

    def payment(self, lump_sum, emi_no):
        """
        lumpsum is done after that emi_no
        """
        self.txn_log[emi_no] = lump_sum

    def balance(self, emi_num):
        """
        return the total amount paid after emi_num
        """
        total_lumpsum = 0
        for k in self.txn_log.keys():
            if k <= emi_num:
                total_lumpsum += self.txn_log[k]
        total_emi_amount_paid = self.monthly_emi * emi_num
        paid_amount = total_lumpsum + total_emi_amount_paid
        remaining_amount = self.repay_amount - paid_amount

        if paid_amount >= self.repay_amount:
            emi_remaining = 0
        elif self.monthly_emi > remaining_amount:
            emi_remaining = 1
        else:
            emi_remaining = math.ceil(remaining_amount / self.monthly_emi)
        return paid_amount, emi_remaining



class InputHandler:
    """
    Class for streaming input and processing it
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.banks = {}

    def process(self):
        with open(self.input_file) as f:
            for line in f:
                self.process_line(line)

    def process_line(self, line):
        args = line.split(" ")
        action = args[0]
        bank = args[1]
        borrower_name = args[2]

        if bank not in self.banks.keys():
            self.banks[bank] = Bank(bank)

        bank_o = self.banks[bank]

        # based on command take the required action
        if action == Actions.payment.value:
            lump_sum = float(args[3])
            emi_num = float(args[4])
            bank_o.payment(borrower_name, lump_sum, emi_num)
        elif action == Actions.loan.value:
            principal = args[3]
            years = args[4]
            rate = args[5]
            bank_o.loan(borrower_name, principal, years, rate)
        elif action == Actions.balance.value:
            emi_num = float(args[3])
            bank_o.balance(borrower_name, emi_num)
        else:
            print("Invalid action")


if __name__ == "__main__":
    file_path = sys.argv[1]
    ih = InputHandler(file_path)
    ih.process()
