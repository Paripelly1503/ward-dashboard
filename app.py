import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward Election Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    raw = pd.read_excel(uploaded_file, header=None)

    # First row as header
    raw.columns = raw.iloc[0]
    df = raw[1:]

    # Remove blank rows
    df.dropna(how="all", inplace=True)
    df.fillna("", inplace=True)

    # Rename by column POSITION (important)
    df.rename(columns={
        df.columns[4]: "name",
        df.columns[6]: "gender",
        df.columns[7]: "age",
        df.columns[9]: "house"
    }, inplace=True)

    st.success("File loaded successfully!")

    # Sidebar search
    st.sidebar.header("Search Filters")
    house = st.sidebar.text_input("Enter House Number")
    name = st.sidebar.text_input("Enter Name")

    filtered = df.copy()

    if house:
        filtered = filtered[
            filtered["house"].astype(str).str.contains(house, case=False)
        ]

    if name:
        filtered = filtered[
            filtered["name"].astype(str).str.contains(name, case=False)
        ]

    # Metrics
    c1, c2 = st.columns(2)
    c1.metric("Total Members Found", len(filtered))
    c2.metric("Unique Houses", filtered["house"].nunique())

    st.divider()

    # Table
    st.subheader("Matching Members")
    st.dataframe(
        filtered[["name", "house", "gender", "age"]],
        use_container_width=True
    )

    # Gender Pie
    st.divider()
    st.subheader("Gender Distribution")
    fig = px.pie(filtered, names="gender")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
