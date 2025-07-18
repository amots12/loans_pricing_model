# Loan Pricing Module

A Python module for pricing performing loan portfolios using discounted cash flow (DCF) methods. This model is tailored for asset buyers or analysts evaluating loans with varying borrower rates, credit scores, tenors, and servicing costs.

---

## 🔧 Features

- Supports multiple loan products (e.g., `PV`, `EHP`) via class inheritance
- Calculates monthly cash flow waterfalls per loan
- Applies credit losses, prepayments, and servicing fees
- Discounts net cash flows using investor’s required return
- Outputs loan-level purchase prices with metadata

---

## 🧩 5D Pricing Framework

The model supports pricing points across **five dimensions**:

1. **Product Type**: Loan structure (e.g., amortization style)
2. **Customer Interest Rate**: Nominal rate paid by borrower
3. **Credit Score**: Risk segment for default assumptions
4. **Tenor**: Loan term in months
5. **Servicing Fee**: Fee charged for managing the loan

Each loan is priced by simulating its cash flows and applying these assumptions dynamically.

---

## 🧾 Required Inputs

### 📄 Loan Tape (as DataFrame or CSV)
Each row represents one loan with the following fields:

- `Loan_ID`
- `Principal`
- `Interest_Rate`
- `Term`
- `Origination_Date`
- `Seasoning`
- `Credit_Rating`
- `Product_Type`
- `Servicing_Fee` (optional)

### ⚙️ Assumptions (Python dictionary or config file)
```python
assumptions = {
    'discount_rate': 0.045,
    'cpr_monthly': 0.02,
    'monthly_loss_rate': 0.000083,
    'servicing_fee': 0.0025  # default if not set per loan
}
