import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    raw = pd.read_excel(uploaded_file, header=None)

    # First row as header
    raw.columns = raw.iloc[0]
    df = raw.iloc[1:]

    # Remove empty rows
    df = df.dropna(how="all")

    # Convert entire dataframe to string
    df = df.astype(str)

    # Map required columns by index
    df["NAME"] = df.iloc[:,4]
    df["GENDER"] = df.iloc[:,6]
    df["AGE"] = df.iloc[:,7]
    df["HOUSE"] = df.iloc[:,9]

    st.success("File loaded successfully!")

    # Sidebar search
    st.sidebar.header("Search Filters")
    name_input = st.sidebar.text_input("Enter Name")
    house_input = st.sidebar.text_input("Enter House Number")

    filtered = df.copy()

    if name_input != "":
        filtered = filtered[filtered["NAME"].apply(lambda x: name_input.lower() in x.lower())]

    if house_input != "":
        filtered = filtered[filtered["HOUSE"].apply(lambda x: house_input.lower() in x.lower())]

    # Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Members Found", len(filtered))

    unique_houses = list(set(filtered["HOUSE"]))
    unique_houses = [h for h in unique_houses if h.strip() != ""]
    col2.metric("Unique Houses", len(unique_houses))

    st.divider()

    # Table
    st.subheader("Matching Members")
    st.dataframe(filtered[["NAME","HOUSE","GENDER","AGE"]], use_container_width=True)

    # Gender Pie
    st.divider()
    st.subheader("Gender Distribution")
    fig = px.pie(filtered, names="GENDER")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
