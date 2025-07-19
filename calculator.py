from loan_pricing_module import PVLoan, EHPLoan
import pandas as pd

def price_loan_book(loan_tape, assumptions):
    results = []
    for _, row in loan_tape.iterrows():
<<<<<<< HEAD
        if row['Product_Type'] == 'PV':
            loan = PVLoan(row, assumptions)
        elif row['Product_Type'] == 'EHP':
=======
        if row['Product_Type'] == 'Level_Payment_Loan':
            loan = PVLoan(row, assumptions)
        elif row['Product_Type'] == 'Equal_Principal_Loan':
>>>>>>> dc8932e (Refactored project: descriptive product types, updated README and license)
            loan = EHPLoan(row, assumptions)
        else:
            continue

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