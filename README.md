# Loan Pricing Module

This project implements a Python-based calculator for pricing performing loan portfolios using a DCF model.

## Features
- Supports multiple product types (Auto, Bike)
- Accounts for customer interest rate, credit score, tenor, servicing fee
- Discounts net cash flows using investor rate
- YAML-configurable assumptions

## Inputs
- `inputs/loan_tape.csv`: Loan-level data
- `inputs/config.yaml`: Global assumptions

## Outputs
- `outputs/priced_loans.csv`

## Run Example
```bash
python main.py --tape inputs/loan_tape.csv --config inputs/config.yaml --output outputs/priced_loans.csv
```
