import pandas as pd
import numpy as np

class LoanProduct:
    def __init__(self, loan_row: pd.Series, assumptions: dict, forward_curve: dict = None, pd_curves: dict = None):
        self.loan_id = loan_row['Loan_ID']
        self.principal = loan_row['Principal']
        self.term = loan_row['Term']
        self.start_date = pd.to_datetime(loan_row['Origination_Date'])
        self.seasoning = loan_row.get('Seasoning', 0)
        self.credit_rating = loan_row.get('Credit_Rating', 'A')
        self.product_type = loan_row['Product_Type']
        self.fee = loan_row.get('Servicing_Fee', assumptions.get('servicing_fee', 0))
        self.assumptions = assumptions
        self.forward_curve = forward_curve or {}
        self.pd_curves = pd_curves or {}

        self.lgd = assumptions.get("lgd", 1.0)
        self.rate_type = loan_row.get('Rate_Type', 'Fixed')
        if self.rate_type == 'Floating':
            self.margin = loan_row.get('Margin', 0.02)
        else:
            self.fixed_rate = loan_row['Interest_Rate']

    def get_monthly_rate(self, month):
        if self.rate_type == 'Floating':
            index_rate = self.forward_curve.get(month, self.forward_curve.get('default', 0.02))
            return (index_rate + self.margin) / 12
        else:
            return self.fixed_rate / 12

    def get_monthly_pd(self, month):
        rating = self.credit_rating
        return self.pd_curves.get(rating, {}).get(str(month), 0.0)

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
        balance = self.principal
        cashflows = []
        first_month_rate = self.get_monthly_rate(1)
        annuity = np.pmt(first_month_rate, months, -self.principal)

        for m in range(1, months + 1):
            rate = self.get_monthly_rate(m)
            pd = self.get_monthly_pd(m)
            interest = balance * rate
            principal = annuity - interest
            balance -= principal

            prepayment = balance * self.assumptions.get('cpr_monthly', 0)
            loss = balance * pd * self.lgd
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
        balance = self.principal
        principal_payment = self.principal / months
        cashflows = []

        for m in range(1, months + 1):
            rate = self.get_monthly_rate(m)
            pd = self.get_monthly_pd(m)
            interest = balance * rate
            balance -= principal_payment

            prepayment = balance * self.assumptions.get('cpr_monthly', 0)
            loss = balance * pd * self.lgd
            servicing_fee = self.fee * (interest + principal_payment)

            net_cf = interest + principal_payment - servicing_fee - loss
            cashflows.append({
                'Month': m,
                'Annuity': interest + principal_payment,
                'Interest': interest,
                'Principal': principal_payment,
                'Prepayment': prepayment,
                'Loss': loss,
                'Servicing': servicing_fee,
                'Net_Cashflow': net_cf
            })

        return pd.DataFrame(cashflows)