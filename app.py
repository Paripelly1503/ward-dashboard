import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    # Read excel raw
    raw = pd.read_excel(uploaded_file, header=None)

    # First row becomes header
    raw.columns = raw.iloc[0]
    df = raw.iloc[1:].copy()

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Replace NaN with empty string
    df = df.fillna("")

    # Rename by fixed positions (based on your file)
    df.rename(columns={
        df.columns[4]: "NAME",
        df.columns[6]: "GENDER",
        df.columns[7]: "AGE",
        df.columns[9]: "HOUSE"
    }, inplace=True)

    # Force everything to string
    df["NAME"] = df["NAME"].astype(str)
    df["HOUSE"] = df["HOUSE"].astype(str)
    df["GENDER"] = df["GENDER"].astype(str)
    df["AGE"] = df["AGE"].astype(str)

    st.success("File loaded successfully!")

    # ------------------
    # SEARCH
    # ------------------
    st.sidebar.header("Search Filters")
    name_input = st.sidebar.text_input("Enter Name")
    house_input = st.sidebar.text_input("Enter House Number")

    filtered = df.copy()

    if name_input:
        filtered = filtered[filtered["NAME"].str.contains(name_input, case=False)]

    if house_input:
        filtered = filtered[filtered["HOUSE"].str.contains(house_input, case=False)]

    # ------------------
    # METRICS
    # ------------------
    col1, col2 = st.columns(2)

    col1.metric("Total Members Found", len(filtered))

    unique_houses = filtered["HOUSE"].unique()
    unique_houses = [h for h in unique_houses if h.strip() != ""]
    col2.metric("Unique Houses", len(unique_houses))

    st.divider()

    # ------------------
    # TABLE
    # ------------------
    st.subheader("Matching Members")
    st.dataframe(
        filtered[["NAME", "HOUSE", "GENDER", "AGE"]],
        use_container_width=True
    )

    # ------------------
    # GENDER PIE
    # ------------------
    st.divider()
    st.subheader("Gender Distribution")
    fig = px.pie(filtered, names="GENDER")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
