import streamlit as st
import pandas as pd
import numpy as np
from math import log, sqrt, exp
from scipy.stats import norm

st.set_page_config(page_title="USD/INR Option Calculator", page_icon="💱", layout="wide")

# --------------------------------------------
# FUNCTIONS
# --------------------------------------------

def fx_black_scholes(S, K, T, r_d, r_f, vol, option_type):
    """FX Black-Scholes Model"""
    try:
        d1 = (np.log(S / K) + (r_d - r_f + 0.5 * vol * vol) * T) / (vol * np.sqrt(T))
        d2 = d1 - vol * np.sqrt(T)

        if option_type == "Call":
            price = S * exp(-r_f * T) * norm.cdf(d1) - K * exp(-r_d * T) * norm.cdf(d2)
        else:
            price = K * exp(-r_d * T) * norm.cdf(-d2) - S * exp(-r_f * T) * norm.cdf(-d1)

        return round(price, 4)
    except:
        return 0.0


# --------------------------------------------
# PAGE TITLE
# --------------------------------------------

st.title("💱 USD/INR Forex Option Calculator & Option Chain")
st.write("A clean UI app to calculate FX options & display USD/INR option chain.")

tab1, tab2 = st.tabs(["📊 Option Chain (USD/INR)", "🧮 Option Calculator"])


# --------------------------------------------
# TAB 1 — OPTION CHAIN
# --------------------------------------------

with tab1:
    st.header("📊 USD/INR Option Chain")

    strikes = [82, 82.25, 82.5, 82.75, 83, 83.25, 83.5, 83.75, 84]
    calls = [0.60, 0.52, 0.45, 0.39, 0.32, 0.28, 0.25, 0.22, 0.20]
    puts =  [0.20, 0.24, 0.28, 0.34, 0.40, 0.46, 0.52, 0.60, 0.68]

    df = pd.DataFrame({
        "Strike": strikes,
        "Call Price": calls,
        "Put Price": puts
    })

    st.dataframe(df, use_container_width=True)


# --------------------------------------------
# TAB 2 — OPTION CALCULATOR
# --------------------------------------------

with tab2:
    st.header("🧮 USD/INR Option Calculator")

    col1, col2 = st.columns(2)

    with col1:
        S = st.number_input("💵 Spot Price (USD/INR)", min_value=1.0, value=83.00)
        F = st.number_input("📈 Future Price (USD/INR)", min_value=1.0, value=83.20)
        K = st.number_input("🎯 Strike Price", min_value=1.0, value=83.00)
        vol = st.number_input("📉 Volatility (in %)", min_value=1.0, value=6.0) / 100

    with col2:
        T = st.number_input("⏳ Time to Expiry (Years)", min_value=0.001, value=0.083)
        r_d = st.number_input("🏦 Domestic Interest Rate (INR %)", min_value=0.0, value=6.5) / 100
        r_f = st.number_input("🌎 Foreign Interest Rate (USD %)", min_value=0.0, value=5.0) / 100
        option_type = st.selectbox("Option Type", ["Call", "Put"])

    if st.button("Calculate Option Price"):
        price = fx_black_scholes(S, K, T, r_d, r_f, vol, option_type)
        st.success(f"💰 {option_type} Option Price: {price}")


# --------------------------------------------
# END
# --------------------------------------------
