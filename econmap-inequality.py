import streamlit as st
import plotly.express as px
import numpy as np

# Title
st.title("EconMap: Inequality Policy Simulator")
st.markdown("Test how policies affect wealth inequality (Gini coefficient).")

# Policy sliders
st.sidebar.header("Policy Levers")
ubi = st.sidebar.slider("UBI (Monthly $)", 0, 2000, 500)
tax_rate = st.sidebar.slider("Top 1% Tax Rate (%)", 0, 70, 30)
education_spending = st.sidebar.slider("Education Spending Increase (%)", 0, 100, 10)

# Simulate wealth distribution
def generate_wealth(ubi, tax_rate, education_spending):
    np.random.seed(42)
    wealth = np.random.pareto(1.5, 1000) * 100_000  # Pareto distribution (realistic inequality)
    
    # Apply policies
    wealth += ubi * 12  # UBI
    wealth[wealth > np.percentile(wealth, 99)] *= (1 - tax_rate/100)  # Tax top 1%
    wealth *= (1 + education_spending/200)  # Education boosts mobility
    
    return wealth

# Calculate Gini coefficient
def gini(wealth):
    wealth = sorted(wealth)
    n = len(wealth)
    cum_wealth = np.cumsum(wealth)
    return (n + 1 - 2 * np.sum(cum_wealth) / cum_wealth[-1]) / n

# Run simulation
wealth = generate_wealth(ubi, tax_rate, education_spending)
gini_index = gini(wealth)

# Visualizations
col1, col2 = st.columns(2)
with col1:
    st.metric("Gini Coefficient", f"{gini_index:.2f}", 
              delta=f"{(0.65 - gini_index):.2f} vs. baseline" if gini_index < 0.65 else "")
with col2:
    st.metric("Median Wealth", f"${int(np.median(wealth)):,}")

fig = px.histogram(wealth, nbins=50, labels={'value': 'Wealth'}, 
                   title="Wealth Distribution After Policies")
st.plotly_chart(fig)

# Policy explanation
st.markdown("""
### How Policies Work:
- **UBI**: Adds flat income to all (reduces poverty).
- **Top 1% Tax**: Redistributes from richest (lowers inequality).
- **Education Spending**: Increases mobility (long-term equality).
""")
