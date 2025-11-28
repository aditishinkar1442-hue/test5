import streamlit as st
import pandas as pd

st.set_page_config(page_title="USD/INR Option Calculator", page_icon="💹", layout="wide")

# --------------------- HEADER ---------------------
st.title("💹 USD/INR Options Chain + Option Calculator")

st.markdown("""
This app shows the **USD/INR Options Chain**, highlights **ATM / ITM / OTM**, 
and provides an **Option Calculator** for quick analysis.
""")

st.divider()

# --------------------- INPUTS ---------------------

col1, col2, col3 = st.columns(3)

with col1:
    spot = st.number_input("💰 Spot Price (USD/INR)", min_value=70.0, max_value=95.0, value=83.20, step=0.01)

with col2:
    future = st.number_input("📈 Future Price (USD/INR)", min_value=70.0, max_value=100.0, value=83.50, step=0.01)

with col3:
    strikes_range = st.number_input("🔢 Number of Strikes (above & below ATM)", min_value=3, max_value=15, value=6)

st.divider()

# --------------------- OPTION CHAIN TABLE ---------------------

st.subheader("📊 USD/INR Options Chain (Highlighted ATM / ITM / OTM)")

# Generate strikes around spot price
atm_strike = round(spot)
strikes = [atm_strike + i for i in range(-strikes_range, strikes_range + 1)]

data = {
    "Strike": strikes,
    "Call Premium (Fake Data)": [abs(spot - s) + 1 for s in strikes],
    "Put Premium (Fake Data)": [abs(s - spot) + 1 for s in strikes]
}

df = pd.DataFrame(data)

# Classification (ATM / ITM / OTM)
def classify_option(strike, spot):
    if strike == round(spot):
        return "ATM"
    elif strike < spot:
        return "Call ITM / Put OTM"
    else:
        return "Call OTM / Put ITM"

df["Option Type"] = df["Strike"].apply(lambda s: classify_option(s, spot))

# Colors
def highlight_row(row):
    if row["Option Type"] == "ATM":
        return ['background-color: yellow'] * len(row)
    elif "ITM" in row["Option Type"]:
        return ['background-color: lightgreen'] * len(row)
    else:
        return ['background-color: lightcoral'] * len(row)

st.dataframe(df.style.apply(highlight_row, axis=1), use_container_width=True)

st.divider()


# --------------------- OPTION CALCULATOR ---------------------

st.subheader("🧮 Option Calculator")

colA, colB, colC = st.columns(3)

with colA:
    calc_strike = st.number_input("Strike Price", min_value=70.0, max_value=100.0, value=atm_strike, step=0.5)

with colB:
    premium = st.number_input("Premium Paid (₹)", min_value=0.1, max_value=50.0, value=2.5, step=0.1)

with colC:
    option_type = st.selectbox("Option Type", ["Call", "Put"])

# Payoff Calculation
if option_type == "Call":
    intrinsic = max(spot - calc_strike, 0)
else:
    intrinsic = max(calc_strike - spot, 0)

profit_loss = intrinsic - premium

colP, colQ = st.columns(2)

with colP:
    st.metric(label="Intrinsic Value", value=f"₹{intrinsic:.2f}")

with colQ:
    st.metric(label="Profit / Loss", value=f"₹{profit_loss:.2f}")

st.success("Calculator Ready — No SciPy Needed. Fully Deployable on Streamlit Cloud.")
