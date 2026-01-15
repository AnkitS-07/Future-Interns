import streamlit as st
import pandas as pd

st.title("📊 Chatbot Analytics Dashboard")

try:
    df = pd.read_csv("chat_logs.csv")
    st.metric("Total Conversations", len(df))
    st.dataframe(df.tail(10))
except FileNotFoundError:
    st.warning("No chat data available yet.")
