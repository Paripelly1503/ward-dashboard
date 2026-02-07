import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward Election Dashboard", layout="wide")
st.title("🗳 Ward Election Member Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # Clean data
    df.dropna(how="all", inplace=True)
    df.fillna("", inplace=True)
    df.columns = df.columns.str.strip().str.lower()

    # Find matching columns automatically
    def find_col(word):
        for c in df.columns:
            if word in c:
                return c
        return None

    house_col = find_col("house")
    fname_col = find_col("first")
    lname_col = find_col("last")
    religion_col = find_col("relig")

    st.success("File loaded successfully!")

    st.sidebar.header("Search Filters")

    house = st.sidebar.text_input("Enter House Number")
    fname = st.sidebar.text_input("Enter First Name")
    lname = st.sidebar.text_input("Enter Last Name")

    filtered = df.copy()

    if house and house_col:
        filtered = filtered[filtered[house_col].astype(str).str.contains(house, case=False)]

    if fname and fname_col:
        filtered = filtered[filtered[fname_col].astype(str).str.contains(fname, case=False)]

    if lname and lname_col:
        filtered = filtered[filtered[lname_col].astype(str).str.contains(lname, case=False)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members Found", len(filtered))

    if house_col:
        col2.metric("Unique Houses", filtered[house_col].nunique())

    if fname_col:
        col3.metric("Unique First Names", filtered[fname_col].nunique())

    st.divider()

    st.subheader("Matching Members")
    st.dataframe(filtered, use_container_width=True)

    if religion_col:
        st.divider()
        st.subheader("Religion Distribution")
        fig = px.pie(filtered, names=religion_col)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
