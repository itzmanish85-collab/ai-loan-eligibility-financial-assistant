import streamlit as st

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "eligibility" not in st.session_state:
    st.session_state.eligibility = None

if "emi_result" not in st.session_state:
    st.session_state.emi_result = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

from src.emi import calculate_emi
from src.eligibility import check_eligibility
from src.recommendation import recommend_products
from src.ai_assistant import generate_ai_explanation
st.sidebar.title("Loan Assistant")

page = st.sidebar.radio(
    "Navigate",
    [
        "Loan Assessment",
        "AI Assistant",
        "Product Insights"
    ]
)


if page == "Loan Assessment":
    st.title("🤖 AI Loan Eligibility & Financial Guidance Assistant")
    st.write("Enter your information to get an illustrative loan assessment.")

elif page == "AI Assistant":
    st.title("💬 AI Financial Assistant")
    st.write("Ask questions about your loan assessment.")

elif page == "Product Insights":
    st.title("📊 Product Insights")
    st.write("Product analytics and experimentation dashboard.")

    st.subheader("Key Product Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Assessment Completion", "78%")
    col2.metric("AI Assistant Usage", "64%")
    col3.metric("Recommendation CTR", "42%")

    st.subheader("Product Funnel")

    st.write("👤 Users entering loan information → 100%")
    st.write("📊 Users completing assessment → 78%")
    st.write("🎯 Users viewing recommendations → 61%")
    st.write("💬 Users asking AI questions → 50%")

    st.subheader("💡 Product Insight")

    st.info(
        "The biggest opportunity is improving the transition "
        "from loan assessment to AI-assisted guidance. "
        "A conversational assistant could help users understand "
        "eligibility, EMI affordability and recommended products."
    )

    st.subheader("🧪 Experiment Idea")

    st.write(
        "**A/B Test:** Compare the standard loan result page "
        "with a conversational AI guidance experience."
    )

    st.write(
        "**Primary metric:** Recommendation click-through rate"
    )

    st.write(
        "**Secondary metrics:** Assessment completion, "
        "AI assistant usage and user engagement"
    )

st.write(
    "Enter your information to get an illustrative loan assessment."
)
st.warning(
    "⚠️ This is a prototype for educational and product-design purposes. "
    "Eligibility, risk scores, EMI calculations and recommendations are "
    "illustrative and do not represent actual lender decisions."
)

st.header("Applicant Information")

age = st.number_input(
    "Age",
    min_value=18,
    max_value=70,
    value=23
)

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0,
    value=50000
)

credit_score = st.number_input(
    "Credit Score",
    min_value=300,
    max_value=900,
    value=750
)

existing_emi = st.number_input(
    "Existing Monthly EMI (₹)",
    min_value=0,
    value=5000
)

loan_amount = st.number_input(
    "Loan Amount (₹)",
    min_value=10000,
    value=500000
)

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=10.0
)

tenure = st.number_input(
    "Loan Tenure (Years)",
    min_value=1,
    max_value=30,
    value=5
)


if st.button("Analyze My Loan"):
    st.session_state.analysis_done = True

    st.session_state.eligibility = check_eligibility(
        age,
        income,
        credit_score,
        existing_emi
    )

    st.session_state.emi_result = calculate_emi(
        loan_amount,
        interest_rate,
        tenure
    )

    st.session_state.recommendations = recommend_products(
        income,
        credit_score,
        loan_amount
    )


# Show results after analysis
if st.session_state.analysis_done:

    eligibility = st.session_state.eligibility
    emi_result = st.session_state.emi_result
    recommendations = st.session_state.recommendations

    st.header("Assessment Result")

    if eligibility["eligible"]:
        st.success("You pass the illustrative eligibility checks.")
    else:
        st.error("You do not pass all illustrative eligibility checks.")

    st.metric(
        "Eligibility Score",
        f"{eligibility['score']}%"
    )

    st.metric(
        "Estimated Monthly EMI",
        f"₹{emi_result['emi']:,.0f}"
    )

    st.metric(
        "Risk Level",
        eligibility["risk"]
    )

    st.subheader("Eligibility Checks")

    for check, result in eligibility["checks"].items():
        if result:
            st.write(f"✅ {check}")
        else:
            st.write(f"❌ {check}")

    st.subheader("Loan Calculation")

    st.write(
        f"Total repayment: ₹{emi_result['total_payment']:,.0f}"
    )

    st.write(
        f"Total interest: ₹{emi_result['total_interest']:,.0f}"
    )

    st.subheader("Recommended Loan Products")

    if recommendations.empty:
        st.info("No matching synthetic loan products found.")
    else:
        st.dataframe(
            recommendations[
                [
                    "product_name",
                    "loan_type",
                    "interest_rate",
                    "max_amount",
                    "match_score"
                ]
            ],
            hide_index=True
        )

    st.subheader("🤖 AI Financial Guidance")

    ai_explanation = generate_ai_explanation(
        eligibility,
        emi_result,
        recommendations
    )

    st.write(ai_explanation)


    # Chatbot
    st.subheader("💬 Ask the AI Assistant")

    question = st.chat_input(
        "Ask something about your loan assessment..."
    )

    if question:

        st.chat_message("user").write(question)

        answer = generate_ai_explanation(
            eligibility,
            emi_result,
            recommendations,
            question
        )

        st.chat_message("assistant").write(answer)



    

    