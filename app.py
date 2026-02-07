import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Ward Election Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

# ----------------------------
# FILE UPLOAD
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Ward Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    # Read file WITHOUT headers
    raw = pd.read_excel(uploaded_file, header=None)

    # Take first row as header
    raw.columns = raw.iloc[0]
    df = raw[1:]

    # Clean column names
    df.columns = df.columns.astype(str).str.strip().str.lower()

    # Remove blank rows
    df.dropna(how="all", inplace=True)
    df.fillna("", inplace=True)

    # Rename needed columns
    df.rename(columns={
        "name": "name",
        "house no": "house",
        "gender": "gender",
        "age": "age"
    }, inplace=True)

    st.success("File loaded successfully!")

    # ----------------------------
    # SIDEBAR SEARCH
    # ----------------------------
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

    # ----------------------------
    # METRICS
    # ----------------------------
    c1, c2 = st.columns(2)
    c1.metric("Total Members Found", len(filtered))
    c2.metric("Unique Houses", filtered["house"].nunique())

    st.divider()

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("Matching Members")
    st.dataframe(
        filtered[["name","house","gender","age"]],
        use_container_width=True
    )

    # ----------------------------
    # GENDER PIE CHART
    # ----------------------------
    if "gender" in filtered.columns:
        st.divider()
        st.subheader("Gender Distribution")
        fig = px.pie(filtered, names="gender")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
