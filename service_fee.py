import numpy as np

def optimize_service_fee(loan_row, assumptions, model_class, max_pct_price=1.05, fee_step=0.0005):
    start_fee = assumptions.get('start_fee', 0.0025)  # 0.25%
    max_fee = assumptions.get('max_fee', 0.10)

    fee = start_fee
    price = 0

    while fee <= max_fee:
        assumptions['servicing_fee'] = fee
        loan = model_class(loan_row, assumptions)
        price = loan.price()

        principal = loan.principal
        if principal > 0 and price / principal <= max_pct_price:
            break
        fee += fee_step

    return fee, price