import argparse
import pandas as pd
from calculator import price_loan_book
from utils import load_yaml_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loan Book Purchase Price Calculator")
    parser.add_argument("--tape", type=str, required=True, help="Path to loan tape CSV file")
    parser.add_argument("--config", type=str, required=True, help="Path to assumptions YAML file")
    parser.add_argument("--output", type=str, default="priced_loans.csv", help="Output CSV file")

    args = parser.parse_args()
    tape_df = pd.read_csv(args.tape)
    assumptions = load_yaml_config(args.config)

    results = price_loan_book(tape_df, assumptions)
    results.to_csv(args.output, index=False)
    print(f"Pricing completed. Results saved to {args.output}")