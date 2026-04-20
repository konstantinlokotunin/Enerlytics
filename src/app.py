import streamlit as st
import pandas as pd
from extract import extract_data
from transform import transform_data
from visualization import visualize_data

st.set_page_config(layout="wide")

st.title("⚡ Enerlytics Dashboard")
st.markdown("#### European Energy Market Intelligence")

st.markdown("---")

# Load data
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

if show_raw:
    st.markdown("### 🧾 Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")

df["Date"] = df["Date"].dt.date

st.markdown("### 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Avg EU Gasoline", f"{filtered_df.iloc[:,1].mean():.2f} €/L")
col2.metric("Max Price", f"{filtered_df.iloc[:,1].max():.2f} €/L")
col3.metric("Min Price", f"{filtered_df.iloc[:,1].min():.2f} €/L")

st.markdown("---")

st.markdown("### 🧠 Insights")

avg_price = filtered_df.iloc[:,1].mean()

if avg_price > 2.1:
    st.warning("Current gasoline prices are highly elevated compared to historical levels.")
elif 1.7 < avg_price < 2.1:
    st.warning("Current gasoline prices are elevated compared to historical levels.")
else:
    st.success("Current gasoline prices are relatively stable compared to historical levels.")

tab1 st.tabs("📈 Dashboard")

with tab1:
    st.markdown("### 📈 Fuel Price Trends")

    fig = visualize_data(filtered_df, window)
    st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")
