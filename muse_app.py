import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample ZIP-to-data mapping (you can expand this with real data)
zip_data = {
    "10001": {
        "COLI": 100,
        "effective_tax_rate": 0.30,
        "housing_cost": 40000,
        "refund_or_liability": 500,
        "deduction_ratio": 0.08,
        "net_pay": 50000,
        "post_boost_pay": 52000
    },
    "90210": {
        "COLI": 90,
        "effective_tax_rate": 0.28,
        "housing_cost": 35000,
        "refund_or_liability": 100,
        "deduction_ratio": 0.10,
        "net_pay": 60000,
        "post_boost_pay": 60500
    }
}

# Functions for normalization
def normalize_coli(coli):
    return coli / 100

def normalize_tax_rate(rate):
    return 1 - rate  # lower is better

def normalize_agi(agi):
    return min(agi / 150000, 1)

def normalize_housing(housing_cost, agi):
    burden = housing_cost / agi
    return 1 - min(burden, 1)

def normalize_deduction(ratio):
    if ratio >= 0.10:
        return 1.0
    elif ratio >= 0.05:
        return 0.5
    else:
        return 0.0

def normalize_refund(refund):
    refund = abs(refund)
    if refund <= 250:
        return 1.0
    elif refund > 2500:
        return 0.3
    else:
        return max(0.3, 1 - (refund - 250) / 2250 * 0.7)

def normalize_liquidity(net_pay, adjusted_income):
    ratio = net_pay / adjusted_income
    return min(ratio / 1.5, 1.0)

def normalize_boost(delta):
    if delta >= 250:
        return 1.0
    elif delta >= 100:
        return 0.8
    elif delta > 0:
        return 0.6
    elif delta == 0:
        return 0.5
    else:
        return 0.3

def calculate_muse_score(agi, zip_code):
    data = zip_data.get(zip_code)
    if not data:
        return None, "ZIP code not found in dataset."

    coli_score = normalize_coli(data['COLI'])
    tax_score = normalize_tax_rate(data['effective_tax_rate'])
    agi_score = normalize_agi(agi)
    housing_score = normalize_housing(data['housing_cost'], agi)
    deduction_score = normalize_deduction(data['deduction_ratio'])
    refund_score = normalize_refund(data['refund_or_liability'])
    liquidity_score = normalize_liquidity(data['net_pay'], agi)
    delta_score = normalize_boost(data['post_boost_pay'] - data['net_pay'])

    raw_score = (
        0.20 * coli_score +
        0.20 * tax_score +
        0.15 * agi_score +
        0.10 * housing_score +
        0.10 * deduction_score +
        0.10 * refund_score +
        0.10 * liquidity_score +
        0.05 * delta_score
    )

    muse_score = round(350 + (raw_score * 500))

    if muse_score >= 750:
        tier = "🟢 Excellent"
    elif muse_score >= 650:
        tier = "🟡 Good"
    elif muse_score >= 550:
        tier = "🟠 At Risk"
    else:
        tier = "🔴 Financial Stress"

    return muse_score, tier, {
        "COLI Score": coli_score,
        "Tax Score": tax_score,
        "AGI Score": agi_score,
        "Housing Score": housing_score,
        "Deduction Score": deduction_score,
        "Refund Score": refund_score,
        "Liquidity Score": liquidity_score,
        "Boost Score": delta_score
    }

# Streamlit Custom CSS
st.markdown(
    """
    <style>
    .main { background-color: #f0f2f6; }
    .block-container { padding: 2rem 2rem 2rem 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title & Subtitle
st.markdown("<h1 style='text-align: center;'>💸 Muse Score Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Estimate your financial health based on location and income</p>", unsafe_allow_html=True)
st.divider()

# Layout Inputs
col1, col2 = st.columns(2)
with col1:
    agi = st.number_input("Adjusted Gross Income (AGI)", min_value=10000, max_value=200000, step=1000)
with col2:
    zip_code = st.text_input("ZIP Code", max_chars=5)

# Compute
if st.button("Calculate Muse Score"):
    score, tier, components = calculate_muse_score(agi, zip_code)
    if score:
        st.success("🎯 Muse Score Computed!")

        # Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("Muse Score", score)
        col2.metric("Tier", tier)

        # Visualization (Score Bar)
        fig, ax = plt.subplots(figsize=(6, 1))
        ax.barh([0], [score], color='green' if score >= 650 else 'orange')
        ax.set_xlim(350, 850)
        ax.set_yticks([])
        ax.set_title("Your Muse Score")
        st.pyplot(fig)

        # Score Components
        with st.expander("🔍 Show Scoring Details"):
            for k, v in components.items():
                st.write(f"{k}: {v:.2f}")
    else:
        st.error(tier)
