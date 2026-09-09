def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    months = years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }