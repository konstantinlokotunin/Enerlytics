import streamlit as st
import pandas as pd
from extract import extract_data
from transform import transform_data
from visualization import visualize_data

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .stMetric {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡🌍 Enerlytics — Energy Data Platform")
st.markdown("#### European Energy Market Intelligence")

st.markdown("---")

# Load data
st.cache_data(ttl=3600)

df_raw = extract_data()
df = transform_data(df_raw)

st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("Adjust your analysis:")

window = st.sidebar.slider("Rolling Average (days)", 1, 12, 4)
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

show_raw = st.sidebar.checkbox("Show Raw Data")

st.markdown("### 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average EU Gasoline Price", f"{df["EU Gasoline Price (€/L)"].mean():.2f} €/L")
col2.metric("Max Price", f"{df["EU Gasoline Price (€/L)"].max():.2f} €/L")
col3.metric("Min Price", f"{df["EU Gasoline Price (€/L)"].min():.2f} €/L")

latest = df.sort_values("Date", ascending=False).iloc[0]
previous = df.sort_values("Date", ascending=False).iloc[1]

delta = latest["EU Gasoline Price (€/L)"] - previous["EU Gasoline Price (€/L)"]

st.metric(
    "Latest Price",
    f"{latest["EU Gasoline Price (€/L)"]:.2f} €/L",
    f"{delta:+.2f} €/L"
)

st.markdown("---")

st.markdown("### 🧠 Insights")

latest_price = latest["EU Gasoline Price (€/L)"]
avg_price = df["EU Gasoline Price (€/L)"].mean()

if latest_price > avg_price * 1.12:
    regime = "High price regime"
elif latest_price < avg_price * 0.9:
    regime = "Low price regime"
else:
    regime = "Normal range"

st.info(f"Market regime: {regime}")

st.markdown("---")

st.markdown("### 📈 Fuel Analysis Dashboard")

fig1, fig2, fig3, fig4 = visualize_data(filtered_df, window)

tab1, tab2, tab3, tab4 = st.tabs(["Prices (EU)", "Volatility (EU)", "Spreads (EU vs AT)", "Spreads (EU Petrol vs EU Diesel)"])

with tab1:
    st.pyplot(fig1, width="stretch")
with tab2:
    st.pyplot(fig2, width="stretch")
with tab3:
    st.pyplot(fig3, width="stretch")
with tab4:
    st.pyplot(fig4, width="stretch")

last_date = df["Date"].max()

st.caption(f"🟢 **Last updated:** {last_date.strftime("%Y-%m-%d")}")

st.markdown("---")

if show_raw:
    st.markdown("### 🧾 Raw Data")

    df_display = filtered_df.copy()
    df_display["Date"] = df_display["Date"].dt.strftime("%Y-%m-%d")
    
    st.dataframe(df_display, use_container_width=True)

    st.markdown("---")