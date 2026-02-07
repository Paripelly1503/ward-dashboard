import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Ward 26 Voter Dashboard",
    layout="wide"
)

st.title("🗳 Ward 26 Voter Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file:

    raw = pd.read_excel(uploaded_file, header=None)
    raw.columns = raw.iloc[0]
    df = raw.iloc[1:].copy()

    df = df.dropna(how="all")
    df = df.fillna("")

    # Map required columns
    df["NAME"] = df.iloc[:,4].astype(str)
    df["GENDER"] = df.iloc[:,6].astype(str)
    df["AGE"] = df.iloc[:,7].astype(str)
    df["HOUSE"] = df.iloc[:,9].astype(str)

    # ----------------------------
    # CLEAN GENDER
    # ----------------------------
    def clean_gender(x):
        x = x.strip().upper()
        if x == "M":
            return "Male"
        elif x == "F":
            return "Female"
        else:
            return "Unknown"

    df["GENDER"] = df["GENDER"].apply(clean_gender)

    st.success("File loaded successfully")

    # ----------------------------
    # SIDEBAR SEARCH
    # ----------------------------
    st.sidebar.header("🔍 Search")

    house_input = st.sidebar.text_input("House Number")
    name_input = st.sidebar.text_input("Name")

    filtered = df.copy()

    if house_input:
        filtered = filtered[filtered["HOUSE"].str.contains(house_input, case=False)]

    if name_input:
        filtered = filtered[filtered["NAME"].str.contains(name_input, case=False)]

    # ----------------------------
    # TOP METRICS
    # ----------------------------
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Members", len(filtered))
    c2.metric("Unique Houses", filtered["HOUSE"].nunique())
    c3.metric("Male %", round((filtered["GENDER"]=="Male").mean()*100,1))

    st.divider()

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📋 Members List")

    st.dataframe(
        filtered[["NAME","HOUSE","GENDER","AGE"]],
        use_container_width=True
    )

    st.divider()

    # ----------------------------
    # GENDER PIE
    # ----------------------------
    st.subheader("👥 Gender Distribution")

    gender_counts = filtered["GENDER"].value_counts().reset_index()
    gender_counts.columns = ["Gender","Count"]

    fig = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        hole=0.4,
        title="Male vs Female vs Unknown"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload Excel to start")
