# 📘 Loan Pricing Module (with Conditional PD Curves)

This Python module prices loan portfolios using discounted cash flows, supporting both **fixed** and **floating-rate** loans. It now includes:
- 📉 Conditional Probability of Default (PD) curves
- 🏦 Loss estimation using PD × LGD
- 🧮 Two amortization structures: Level Payment and Equal Principal

---

## 📂 Files

```
loan_pricing/
├── loan_pricing_module.py
├── inputs/
│   ├── config.yaml
│   └── conditional_pd_curves.json
```

---

## 🧾 Inputs

### 🔧 `config.yaml`

```yaml
discount_rate: 0.045
cpr_monthly: 0.02
servicing_fee: 0.0025
lgd: 0.45
```

### 📊 `conditional_pd_curves.json`

Monthly PDs by credit rating (used for expected loss calculation):

```json
{
  "A": { "1": 0.0001, "2": 0.0001, "...": "..." },
  "B": { "6": 0.0002, "7": 0.0002, "...": "..." },
  "C": { "6": 0.0005, "7": 0.0005, "...": "..." }
}
```

---

## 🚀 Usage

Integrate this module in your loan pricing pipeline and call the `price()` method per loan.

---