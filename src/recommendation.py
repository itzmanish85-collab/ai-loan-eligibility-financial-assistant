import pandas as pd


def recommend_products(income, credit_score, loan_amount):
    products = pd.read_csv("data/loan_products.csv")

    eligible_products = products[
        (products["min_income"] <= income)
        & (products["min_credit_score"] <= credit_score)
        & (products["max_amount"] >= loan_amount)
    ].copy()

    if eligible_products.empty:
        return eligible_products

    eligible_products["match_score"] = (
        100
        - abs(credit_score - eligible_products["min_credit_score"]) * 0.1
        - abs(income - eligible_products["min_income"]) / 10000
    )

    eligible_products = eligible_products.sort_values(
        "match_score",
        ascending=False
    )

    return eligible_products.head(3)