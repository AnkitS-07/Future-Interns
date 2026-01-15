import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction Dashboard",
    page_icon="📉",
    layout="wide"
)

# --------------------------------------------------
# Load Model
# --------------------------------------------------
model = joblib.load("churn_model.pkl")

# --------------------------------------------------
# App Title
# --------------------------------------------------
st.title("📉 Customer Churn Prediction System")
st.markdown(
    "Predict customer churn probability and identify high-risk customers for retention strategies."
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("🔧 Options")
mode = st.sidebar.radio(
    "Choose Mode:",
    ["Single Customer Prediction", "Batch Prediction (CSV Upload)"]
)

# --------------------------------------------------
# Feature Input (Manual)
# --------------------------------------------------
if mode == "Single Customer Prediction":
    st.subheader("🧍 Single Customer Churn Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=12)
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
        total_charges = st.number_input("Total Charges", min_value=0.0, value=800.0)

    with col2:
        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"]
        )
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        )

    with col3:
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    # Convert inputs to model-friendly format
    input_data = pd.DataFrame({
        "tenure": [tenure],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
        "Partner": [1 if partner == "Yes" else 0],
        "Dependents": [1 if dependents == "Yes" else 0],
        "PaperlessBilling": [1 if paperless == "Yes" else 0],
        "Contract_One year": [1 if contract == "One year" else 0],
        "Contract_Two year": [1 if contract == "Two year" else 0],
        "PaymentMethod_Electronic check": [1 if payment_method == "Electronic check" else 0]
    })

    # Ensure missing columns exist
    for col in model.feature_names_in_:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[model.feature_names_in_]

    if st.button("🔍 Predict Churn"):
        churn_prob = model.predict_proba(input_data)[0][1]

        st.metric(
            label="Churn Probability",
            value=f"{churn_prob:.2%}"
        )

        if churn_prob > 0.6:
            st.error("⚠ High Risk of Churn")
        elif churn_prob > 0.3:
            st.warning("⚠ Medium Risk of Churn")
        else:
            st.success("✅ Low Risk of Churn")

# --------------------------------------------------
# Batch Prediction
# --------------------------------------------------
else:
    st.subheader("📂 Batch Customer Churn Prediction")

    uploaded_file = st.file_uploader(
        "Upload a CSV file with customer data",
        type=["csv"]
    )

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("📄 Uploaded Data Preview", data.head())

        # Align columns
        for col in model.feature_names_in_:
            if col not in data.columns:
                data[col] = 0

        data = data[model.feature_names_in_]

        churn_probs = model.predict_proba(data)[:, 1]
        data["Churn_Probability"] = churn_probs

        st.write("📊 Churn Predictions", data.head())

        st.download_button(
            label="⬇ Download Predictions",
            data=data.to_csv(index=False),
            file_name="churn_predictions.csv",
            mime="text/csv"
        )

        # Risk Distribution
        st.subheader("📈 Churn Risk Distribution")
        fig, ax = plt.subplots()
        sns.histplot(churn_probs, bins=20, kde=True, ax=ax)
        ax.set_xlabel("Churn Probability")
        ax.set_title("Distribution of Churn Risk")
        st.pyplot(fig)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>Made with 💡 by Ankit Sarkar</p>",
    unsafe_allow_html=True
)
