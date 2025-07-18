# Loan Pricing Module

This project implements a Python-based calculator for pricing performing loan portfolios using a DCF model.

## Features
- Supports multiple amortization types:
  - `Level_Payment_Loan`: Fixed monthly annuity (interest + principal)
  - `Equal_Principal_Loan`: Fixed principal with declining interest
- Accounts for customer interest rate, credit score, tenor, servicing fee
- Discounts net cash flows using investor's discount rate
- Configurable via YAML

## Inputs
- `inputs/loan_tape.csv`: Loan-level data with fields:
  - Loan_ID
  - Principal
  - Interest_Rate
  - Term
  - Origination_Date
  - Seasoning
  - Credit_Rating
  - Product_Type (`Level_Payment_Loan` or `Equal_Principal_Loan`)
  - Servicing_Fee
- `inputs/config.yaml`: Global assumptions like:
  ```yaml
  discount_rate: 0.045
  cpr_monthly: 0.02
  monthly_loss_rate: 0.000083
  servicing_fee: 0.0025
  ```

## Outputs
- `outputs/priced_loans.csv`: Loan-level results with calculated price

## Run Example
```bash
python main.py --tape inputs/loan_tape.csv --config inputs/config.yaml --output outputs/priced_loans.csv
```

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.