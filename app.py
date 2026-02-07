import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    # Load excel without headers
    raw = pd.read_excel(uploaded_file, header=None)

    # First row becomes header
    raw.columns = raw.iloc[0]
    df = raw[1:]

    # Remove blank rows
    df.dropna(how="all", inplace=True)
    df.fillna("", inplace=True)

    # Rename using fixed column positions
    df.rename(columns={
        df.columns[4]: "name",    # NAME
        df.columns[6]: "gender",  # GENDER
        df.columns[7]: "age",     # AGE
        df.columns[9]: "house"   # HOUSE No
    }, inplace=True)

    st.success("File loaded successfully!")

    # -----------------------------------
    # SIDEBAR FILTERS
    # -----------------------------------
    st.sidebar.header("Search Filters")

    name_input = st.sidebar.text_input("Enter Name")
    house_input = st.sidebar.text_input("Enter House Number")

    filtered = df.copy()

    if name_input:
        filtered = filtered[
            filtered["name"].astype(str).str.contains(name_input, case=False)
        ]

    if house_input:
        filtered = filtered[
            filtered["house"].astype(str).str.contains(house_input, case=False)
        ]

    # -----------------------------------
    # METRICS
    # -----------------------------------
    col1, col2 = st.columns(2)

    col1.metric("Total Members Found", len(filtered))

    house_series = filtered["house"].astype(str).str.strip()
    house_series = house_series[house_series != ""]
    col2.metric("Unique Houses", house_series.nunique())

    st.divider()

    # -----------------------------------
    # TABLE
    # -----------------------------------
    st.subheader("Matching Members")
    st.dataframe(
        filtered[["name", "house", "gender", "age"]],
        use_container_width=True
    )

    # -----------------------------------
    # PIE CHART
    # -----------------------------------
    st.divider()
    st.subheader("Gender Distribution")

    fig = px.pie(filtered, names="gender")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
