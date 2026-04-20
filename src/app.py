import streamlit as st
import pandas as pd
from extract import extract_data
from transform import transform_data
from visualization import visualize_data

st.title("⚡🌍 Enerlytics Dashboard")

st.write("Welcome to your European energy market dashboard.")

# Load data
df_raw = extract_data()
df = transform_data(df_raw)

st.write("Data preview:")
st.dataframe(df.head())

st.sidebar.header("Controls")

window = st.sidebar.slider("Smoothing Window", 1, 12, 4)
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Avg EU Gasoline", f"{filtered_df.iloc[:,1].mean():.2f} €/L")
col2.metric("Max Price", f"{filtered_df.iloc[:,1].max():.2f} €/L")
col3.metric("Min Price", f"{filtered_df.iloc[:,1].min():.2f} €/L")
col4.metric("Avg EU Diesel", f"{filtered_df.iloc[:,2].mean():.2f} €/L")
col5.metric("Max Price", f"{filtered_df.iloc[:,2].max():.2f} €/L")
col6.metric("Min Price", f"{filtered_df.iloc[:,2].min():.2f} €/L")

show_raw = st.sidebar.checkbox("Show Raw Data")

if show_raw:
    st.dataframe(filtered_df)

fig = visualize_data(filtered_df, window)

st.pyplot(fig)