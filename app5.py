import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Forex Option Calculator", page_icon="💹", layout="wide")

st.title("💹 USD/INR Forex Option Chain + Option Calculator")

# ----------------------------
# 1) Spot and Future Price
# ----------------------------
spot = st.number_input("💰 Spot Price (USD/INR)", min_value=70.0, max_value=100.0, value=83.20, step=0.10)
future = st.number_input("📈 Future Price (USD/INR)", min_value=70.0, max_value=100.0, value=83.50, step=0.10)

st.write("---")

# -----------------------------------------
# 2) Build Option Chain (ATM / ITM / OTM)
# -----------------------------------------
strikes = [round(spot + i, 2) for i in range(-5, 6)]  # 11 strikes
atm_strike = min(strikes, key=lambda x: abs(x - spot))

chain_data = []
for strike in strikes:
    if strike == atm_strike:
        status = "ATM"
    elif strike > spot:
        status = "OTM"
    else:
        status = "ITM"

    chain_data.append([strike, future - strike, strike - future, status])

df = pd.DataFrame(chain_data, columns=["Strike", "Call IV Price", "Put IV Price", "Option Type"])

# Color function
def color_code(val):
    if val == "ATM":
        return "background-color: yellow; color: black"
    elif val == "ITM":
        return "background-color: lightgreen; color: black"
    else:
        return "background-color: lightblue; color: black"

st.subheader("📊 USD/INR Option Chain")
st.dataframe(df.style.applymap(color_code, subset=["Option Type"]), height=400)

st.write("---")

# ------------------------------
# 3) Option Calculator Section
# ------------------------------
st.header("🧮 Option Price Calculator")

col1, col2 = st.columns(2)

with col1:
    calc_strike = st.number_input(
        "Strike Price",
        min_value=70.0,
        max_value=100.0,
        value=float(atm_strike),   # FIXED ERROR HERE
        step=0.5
    )
    T = st.number_input("⏳ Time to Expiry (Years)", min_value=0.01, max_value=1.0, value=0.0833)
with col2:
    r = st.number_input("📉 Interest Rate (%)", min_value=0.1, max_value=15.0, value=6.0)
    vol = st.number_input("📊 Volatility (%)", min_value=1.0, max_value=50.0, value=10.0)

# ---------------------------------------
# Black-Scholes (WITHOUT SciPy)
# ---------------------------------------
def N(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def black_scholes(F, K, T, r, sigma, type="call"):
    d1 = (math.log(F/K) + (0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if type == "call":
        return math.exp(-r*T)* (F*N(d1) - K*N(d2))
    else:
        return math.exp(-r*T)* (K*N(-d2) - F*N(-d1))

if st.button("Calculate Option Price"):
    call_price = black_scholes(future, calc_strike, T, r/100, vol/100, "call")
    put_price = black_scholes(future, calc_strike, T, r/100, vol/100, "put")

    st.success(f"💵 Call Option Price: {call_price:.4f}")
    st.info(f"📘 Put Option Price: {put_price:.4f}")
