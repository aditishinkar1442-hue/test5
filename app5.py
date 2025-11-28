import streamlit as st
import math

# ===============================
# Black-Scholes Functions (NO SCIPY)
# ===============================
def N(x):
    "Cumulative normal distribution function (approximation)"
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black_scholes(F, K, T, r, sigma, option_type="call"):
    d1 = (math.log(F / K) + (0 + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        return math.exp(-r * T) * (F * N(d1) - K * N(d2))
    else:  # put
        return math.exp(-r * T) * (K * N(-d2) - F * N(-d1))


# ===============================
# PAGE SETTINGS
# ===============================
st.set_page_config(page_title="Forex Option Calculator", page_icon="💹", layout="wide")

st.title("💹 USD/INR Option Chain & Option Calculator")
st.write("A simple and clean app for Forex Options (USD/INR).")


# ===============================
# OPTION CHAIN (DUMMY DATA FOR DISPLAY)
# ===============================
st.subheader("📊 USD/INR Option Chain")

import pandas as pd

strikes = [82, 82.5, 83, 83.5, 84]
calls = [0.20, 0.34, 0.50, 0.75, 1.10]
puts = [1.10, 0.75, 0.50, 0.34, 0.20]

option_chain = pd.DataFrame({
    "Strike Price": strikes,
    "Call Premium (₹)": calls,
    "Put Premium (₹)": puts
})

st.dataframe(option_chain, use_container_width=True)


# ===============================
# OPTION CALCULATOR
# ===============================
st.subheader("🧮 Forex Option Calculator (Black-Scholes)")

col1, col2 = st.columns(2)

with col1:
    F = st.number_input("💱 Future Price (USD/INR)", value=83.0)
    K = st.number_input("🎯 Strike Price", value=83.0)
    sigma = st.number_input("📉 Volatility (σ) in %", value=5.0) / 100

with col2:
    T = st.number_input("⏳ Time to Expiry (Years)", value=0.1)
    r = st.number_input("🏦 Risk-Free Interest Rate (%)", value=6.0) / 100
    option_type = st.selectbox("Option Type", ["call", "put"])


if st.button("Calculate Premium"):
    premium = black_scholes(F, K, T, r, sigma, option_type)
    st.success(f"💰 Option Premium = ₹{premium:.4f}")

