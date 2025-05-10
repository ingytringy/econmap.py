import streamlit as st
import pandas as pd

st.title("💰 EconMap 2.0")
st.write("Now with real country data!")

# Load real-world data
data = pd.read_csv("country_data.csv")

# Country selector
country = st.selectbox("Pick a country", data["country"])
st.write(f"Current inequality in {country}:", data[data["country"]==country]["gini"].values[0])

# Simple policy slider
ubi = st.slider("UBI ($/month)", 0, 1000, 500)
st.write(f"With ${ubi}/month UBI, inequality would drop by {ubi*0.0005:.2f} Gini points")
