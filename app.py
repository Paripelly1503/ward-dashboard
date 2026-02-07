import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file is not None:

    # Read excel without headers
    raw = pd.read_excel(uploaded_file, header=None)

    # First row becomes header
    raw.columns = raw.iloc[0]
    df = raw.iloc[1:].copy()

    # Remove empty rows
    df = df.dropna(how="all")

    # Replace NaN with empty string
    df = df.fillna("")

    # Create clean working columns using fixed positions
    df["NAME"] = df.iloc[:, 4]
    df["GENDER"] = df.iloc[:, 6]
    df["AGE"] = df.iloc[:, 7]
    df["HOUSE"] = df.iloc[:, 9]

    # Convert everything to string
    df["NAME"] = df["NAME"].astype(str)
    df["GENDER"] = df["GENDER"].astype(str)
    df["AGE"] = df["AGE"].astype(str)
    df["HOUSE"] = df["HOUSE"].astype(str)

    st.success("File loaded successfully!")

    # -----------------------------
    # SIDEBAR SEARCH
    # -----------------------------
    st.sidebar.header("Search Filters")

    name_input = st.sidebar.text_input("Enter Name")
    house_input = st.sidebar.text_input("Enter House Number")

    filtered = df.copy()

    if name_input:
        filtered = filtered[
            filtered["NAME"].str.contains(name_input, case=False)
        ]

    if house_input:
        filtered = filtered[
            filtered["HOUSE"].str.contains(house_input, case=False)
        ]

    # -----------------------------
    # METRICS
    # -----------------------------
    col1, col2 = st.columns(2)

    col1.metric("Total Members Found", len(filtered))

    unique_houses = filtered["HOUSE"].unique()
    unique_houses = [h for h in unique_houses if h.strip() != ""]
    col2.metric("Unique Houses", len(unique_houses))

    st.divider()

    # -----------------------------
    # TABLE
    # -----------------------------
    st.subheader("Matching Members")
    st.dataframe(
        filtered[["NAME", "HOUSE", "GENDER", "AGE"]],
        use_container_width=True
    )

    # -----------------------------
    # GENDER PIE CHART
    # -----------------------------
    st.divider()
    st.subheader("Gender Distribution")

    gender_df = pd.DataFrame({
        "Gender": filtered["GENDER"]
    })

    fig = px.pie(gender_df, names="Gender")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Excel file to start.")
