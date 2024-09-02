import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ställ in sidkonfigurationen
st.set_page_config(page_title="Bolånekalkylator", layout="wide")

# Lägg till en titel och beskrivning
st.title("Bolånekalkylator")
st.markdown(
    """
    Använd reglagen nedan för att justera inkomst, kontantinsats och ränta för att se hur de påverkar din månatliga bolånebetalning.
    """
)

# Create sliders for income and down payment
st.sidebar.header("Input Parameters")
income1 = st.sidebar.slider(
    "Inkomst 1", min_value=0, max_value=200000, value=50000, step=1000
)
include_second_income = st.sidebar.checkbox("Inkludera Inkomst 2", value=False)
if include_second_income:
    income2 = st.sidebar.slider(
        "Inkomst 2", min_value=0, max_value=200000, value=50000, step=1000
    )
else:
    income2 = 0
if include_second_income:
    down_payment1 = st.sidebar.slider(
        "Kontantinsats 1", min_value=0, max_value=3000000, value=25000, step=2500
    )
    down_payment2 = st.sidebar.slider(
        "Kontantinsats 2", min_value=0, max_value=3000000, value=25000, step=2500
    )
    down_payment = down_payment1 + down_payment2
else:
    down_payment = st.sidebar.slider(
        "Kontantinsats", min_value=0, max_value=6000000, value=50000, step=5000
    )

# Calculate total income
total_income = income1 + income2


# Function to calculate monthly mortgage payment
def calculate_monthly_payment(
    loan_amount, annual_interest_rate, total_income, down_payment
):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    amortization_rate = 0
    # Simplified stepped amortization function
    if loan_amount >= 4.5 * total_income * 12:
        amortization_rate += 0.01
    if down_payment / loan_amount <= 0.5:
        amortization_rate += 0.01
    if down_payment / loan_amount <= 0.7:
        amortization_rate += 0.01

    amortization = loan_amount * amortization_rate / 12
    interest = loan_amount * monthly_interest_rate

    return amortization, interest


# Generate data for the graph
loan_amounts = range(2000000, 9000001, 100000)
interest_rate = (
    st.sidebar.slider("Ränta", min_value=1.0, max_value=10.0, value=5.0, step=0.1) / 100
)

data = []
for loan_amount in loan_amounts:
    amortization, interest = calculate_monthly_payment(
        loan_amount, interest_rate * 100, total_income, down_payment
    )
    thirty_roof = 100000 + (include_second_income * 100000)
    if interest * 12 > thirty_roof:
        interest_after_tax = ((interest * 12) - thirty_roof) * 0.79 / 12 + (
            thirty_roof / 12
        ) * 0.7
    else:
        interest_after_tax = interest * 0.7
    total = amortization + interest_after_tax
    data.append(
        {
            "Loan Amount": loan_amount,
            "Ränta efter avdrag": interest_after_tax,
            "Amortering": amortization,
            "Totalt": total,
        }
    )

df = pd.DataFrame(data)
df["Total Amount"] = df["Loan Amount"] + down_payment

# Create the interactive graph
st.subheader("Uppdelning av bolånebetalning")
chart = st.line_chart(
    df, x="Total Amount", y=["Ränta efter avdrag", "Amortering", "Totalt"]
)


# Lägg till en tabell för att visa data
st.subheader("Detaljerad data")
st.dataframe(df)
