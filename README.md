# 💸 Muse Score Calculator

The Muse Score™ is a financial wellness score ranging from **350–850**, calculated based on your **Adjusted Gross Income (AGI)** and **ZIP code**. It incorporates key financial factors like cost of living, effective tax rate, housing burden, deduction behavior, and more.

[👉 Click here to try the live app] (https://muse-score-3-iq9a7a3dzk3sbhppwf97xp.streamlit.app/) 

---

## 📈 Features

- ✅ One-click Muse Score estimation using just AGI and ZIP Code
- 📊 Real-time score visualization (bar chart)
- 🧠 Tier classification: Excellent, Good, At Risk, Financial Stress
- 🔍 Scoring breakdown for transparency
- 🎨 Custom UI styling with Streamlit

---

## 🛠 How It Works

1. User enters their **AGI** and **ZIP code**
2. App looks up ZIP-level financial data:
   - Cost of Living Index (COLI)
   - Tax rate
   - Housing costs
   - Deduction and refund behavior
3. The app normalizes each factor and weights them to calculate a raw score.
4. Final Muse Score is scaled between 350–850.

---



