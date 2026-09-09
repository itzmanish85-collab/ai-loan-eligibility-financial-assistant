def check_eligibility(age, income, credit_score, existing_emi):
    checks = {}

    checks["age"] = age >= 21
    checks["income"] = income >= 20000
    checks["credit_score"] = credit_score >= 650

    existing_emi_ratio = existing_emi / income

    checks["existing_emi"] = existing_emi_ratio <= 0.50

    passed = sum(checks.values())
    total = len(checks)

    score = (passed / total) * 100

    if score >= 80:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    eligible = all(checks.values())

    return {
        "eligible": eligible,
        "score": round(score, 2),
        "risk": risk,
        "checks": checks
    }