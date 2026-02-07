import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward Election Dashboard", layout="wide")

st.title("🗳 Ward Election Member Dashboard")

# Upload Excel
uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("File loaded successfully!")

    # Sidebar Filters
    st.sidebar.header("Search Filters")

    house = st.sidebar.text_input("Enter House Number")
    fname = st.sidebar.text_input("Enter First Name")
    lname = st.sidebar.text_input("Enter Last Name")

    filtered = df.copy()

    if house:
        filtered = filtered[filtered["House Number"].astype(str).str.contains(house, case=False)]

    if fname:
        filtered = filtered[filtered["First Name"].str.contains(fname, case=False)]

    if lname:
        filtered = filtered[filtered["Last Name"].str.contains(lname, case=False)]

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members Found", len(filtered))
    col2.metric("Unique Houses", filtered["House Number"].nunique())
    col3.metric("Unique First Names", filtered["First Name"].nunique())

    st.divider()

    # Table
    st.subheader("Matching Members")
    st.dataframe(filtered, use_container_width=True)

    st.divider()

    # Religion Chart
    if "Religion" in df.columns:
        st.subheader("Religion Distribution")
        fig = px.pie(filtered, names="Religion")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")