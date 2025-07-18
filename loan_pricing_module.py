# loan_pricing_module.py

import pandas as pd
import numpy as np
from datetime import datetime

class LoanProduct:
    def __init__(self, loan_row: pd.Series, assumptions: dict):
        self.loan_id = loan_row['Loan_ID']
        self.principal = loan_row['Principal']
        self.rate = loan_row['Interest_Rate']
        self.term = loan_row['Term']
        self.start_date = pd.to_datetime(loan_row['Origination_Date'])
        self.seasoning = loan_row.get('Seasoning', 0)
        self.credit_rating = loan_row.get('Credit_Rating', 'A')
        self.product_type = loan_row['Product_Type']
        self.fee = loan_row.get('Servicing_Fee', assumptions.get('servicing_fee', 0))
        self.assumptions = assumptions

    def calculate_cashflows(self):
        raise NotImplementedError("Each loan product must implement its own cash flow logic.")

    def discount_cashflows(self, cashflows):
        discount_rate = self.assumptions['discount_rate']
        cashflows['Discount_Factor'] = 1 / (1 + discount_rate) ** (cashflows['Month'] / 12)
        cashflows['Discounted_Cashflow'] = cashflows['Net_Cashflow'] * cashflows['Discount_Factor']
        return cashflows

    def price(self):
        cashflows = self.calculate_cashflows()
        discounted = self.discount_cashflows(cashflows)
        return discounted['Discounted_Cashflow'].sum()

class PVLoan(LoanProduct):
    def calculate_cashflows(self):
        months = self.term - self.seasoning
        monthly_rate = self.rate / 12
        annuity = np.pmt(monthly_rate, months, -self.principal)

        cashflows = []
        balance = self.principal

        for m in range(1, months + 1):
            interest = balance * monthly_rate
            principal = annuity - interest
            balance -= principal

            prepayment = balance * self.assumptions.get('cpr_monthly', 0)
            loss = balance * self.assumptions.get('monthly_loss_rate', 0)
            servicing_fee = self.fee * annuity

            net_cf = annuity - servicing_fee - loss
            cashflows.append({
                'Month': m,
                'Annuity': annuity,
                'Interest': interest,
                'Principal': principal,
                'Prepayment': prepayment,
                'Loss': loss,
                'Servicing': servicing_fee,
                'Net_Cashflow': net_cf
            })

        return pd.DataFrame(cashflows)

class EHPLoan(LoanProduct):
    def calculate_cashflows(self):
        months = self.term - self.seasoning
        monthly_rate = self.rate / 12
        balance = self.principal

        cashflows = []
        for m in range(1, months + 1):
            interest = balance * monthly_rate
            repayment = self.principal / months
            balance -= repayment

            prepayment = balance * self.assumptions.get('cpr_monthly', 0)
            loss = balance * self.assumptions.get('monthly_loss_rate', 0)
            servicing_fee = self.fee * (interest + repayment)

            net_cf = interest + repayment - servicing_fee - loss
            cashflows.append({
                'Month': m,
                'Annuity': interest + repayment,
                'Interest': interest,
                'Principal': repayment,
                'Prepayment': prepayment,
                'Loss': loss,
                'Servicing': servicing_fee,
                'Net_Cashflow': net_cf
            })

        return pd.DataFrame(cashflows)

def price_loan_book(loan_tape: pd.DataFrame, assumptions: dict):
    results = []
    for _, row in loan_tape.iterrows():
        if row['Product_Type'] == 'PV':
            loan = PVLoan(row, assumptions)
        elif row['Product_Type'] == 'EHP':
            loan = EHPLoan(row, assumptions)
        else:
            continue  # skip unknown product types

        price = loan.price()
        results.append({
            'Loan_ID': loan.loan_id,
            'Product_Type': loan.product_type,
            'Customer_Rate': loan.rate,
            'Credit_Score': loan.credit_rating,
            'Tenor': loan.term,
            'Servicing_Fee': loan.fee,
            'Price': price
        })

    return pd.DataFrame(results)
