import streamlit as st
import math

st.set_page_config(page_title="USD/INR Options App", page_icon="💹", layout="wide")

# ===== Normal CDF (no scipy needed) =====
def normal_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


# ===== Black Scholes Calculator =====
def black_scholes(F, K, T, r, sigma, option_type):
    d1 = (math.log(F/K) + (0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "CALL":
        price = math.exp(-r*T) * (F*normal_cdf(d1) - K*normal_cdf(d2))
    else:
        price = math.exp(-r*T) * (K*normal_cdf(-d2) - F*normal_cdf(-d1))

    return price


# ===== Sidebar Inputs =====
st.sidebar.header("📌 USD/INR Inputs")

spot = st.sidebar.number_input("Spot Price (USD/INR)", min_value=70.0, max_value=100.0, value=83.30)
future = st.sidebar.number_input("Future Price (USD/INR)", min_value=70.0, max_value=100.0, value=83.50)
vol = st.sidebar.number_input("Volatility (%)", min_value=1.0, max_value=50.0, value=6.0) / 100
rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, value=6.0) / 100
T = st.sidebar.number_input("Time to Expiry (Years)", min_value=0.01, max_value=1.0, value=0.25)

st.title("💹 USD/INR Options Chain + Calculator")


# ===== Option Chain Table =====
st.subheader("📘 USD/INR Option Chain")

strikes = [future - 1.0, future - 0.5, future, future + 0.5, future + 1.0]
strikes = [round(s, 2) for s in strikes]

call_prices = []
put_prices = []
call_status = []
put_status = []

for K in strikes:

    c = black_scholes(future, K, T, rate, vol, "CALL")
    p = black_scholes(future, K, T, rate, vol, "PUT")

    call_prices.append(round(c, 4))
    put_prices.append(round(p, 4))

    # Identify ATM / ITM / OTM
    # Call ITM: F > K
    if future > K:
        call_status.append("ITM")
    elif future == K:
        call_status.append("ATM")
    else:
        call_status.append("OTM")

    # Put ITM: F < K
    if future < K:
        put_status.append("ITM")
    elif future == K:
        put_status.append("ATM")
    else:
        put_status.append("OTM")


import pandas as pd

df = pd.DataFrame({
    "Strike": strikes,
    "CALL Price": call_prices,
    "CALL Status": call_status,
    "PUT Price": put_prices,
    "PUT Status": put_status
})

# Coloring Logic
def color_rows(row):
    color = ""
    if row["CALL Status"] == "ITM":
        color = "background-color: #ffb3b3"   # red-ish
    elif row["CALL Status"] == "ATM":
        color = "background-color: #ffffb3"   # yellow
    elif row["CALL Status"] == "OTM":
        color = "background-color: #b3ffb3"   # green

    # Put separate color shading
    if row["PUT Status"] == "ITM":
        color = "background-color: #ffccff"   # Purple light
    elif row["PUT Status"] == "ATM":
        color = "background-color: #e6e6ff"
    elif row["PUT Status"] == "OTM":
        color = "background-color: #ccffff"

    return [color] * len(row)


st.dataframe(df.style.apply(color_rows, axis=1), use_container_width=True)


# ===== Option Calculator =====
st.subheader("🧮 Option Calculator")

calc_strike = st.number_input("Strike Price", min_value=70.0, max_value=100.0, value=future, step=0.5)
opt_type = st.selectbox("Option Type", ["CALL", "PUT"])

calc_price = black_scholes(future, calc_strike, T, rate, vol, opt_type)

st.success(f"📌 {opt_type} Price: {calc_price:.4f}")

