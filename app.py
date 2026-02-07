import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

uploaded_file = st.file_uploader("Upload Ward Excel File", type=["xlsx"])

if uploaded_file:

    # ---------- LOAD ----------
    raw = pd.read_excel(uploaded_file, header=None)
    raw.columns = raw.iloc[0]
    df = raw.iloc[1:].copy()

    df = df.dropna(how="all")
    df = df.fillna("")

    # Map columns by position
    df["NAME"] = df.iloc[:,4].astype(str)
    df["GENDER"] = df.iloc[:,6].astype(str)
    df["AGE"] = df.iloc[:,7].astype(str)
    df["HOUSE"] = df.iloc[:,9].astype(str)

    # ---------- CLEAN GENDER ----------
    def clean_gender(x):
        x = x.strip().upper()
        if x == "M":
            return "Male"
        elif x == "F":
            return "Female"
        else:
            return ""

    df["GENDER"] = df["GENDER"].apply(clean_gender)

    st.success("File loaded successfully")

    # =====================================
    # 🔍 UNIVERSAL SEARCH BOX
    # =====================================
    st.sidebar.header("Search")

    search_text = st.sidebar.text_input(
        "Type House Number / First Name / Last Name"
    )

    filtered = df.copy()

    if search_text:
        filtered = filtered[
            df["NAME"].str.contains(search_text, case=False) |
            df["HOUSE"].str.contains(search_text, case=False)
        ]

    # =====================================
    # METRICS
    # =====================================
    c1, c2, c3 = st.columns(3)

    c1.metric("Members Found", len(filtered))
    c2.metric("Total Houses", filtered["HOUSE"].nunique())
    c3.metric("Total Voters", len(df))

    st.divider()

    # =====================================
    # TABLE
    # =====================================
    st.subheader("📋 Matching Members")

    st.dataframe(
        filtered[["NAME","HOUSE","GENDER","AGE"]],
        use_container_width=True
    )

    st.divider()

    # =====================================
    # GENDER PIE (ONLY MALE & FEMALE)
    # =====================================
    gender_df = filtered[filtered["GENDER"] != ""]

    gender_counts = gender_df["GENDER"].value_counts().reset_index()
    gender_counts.columns = ["Gender","Count"]

    st.subheader("👥 Male vs Female")

    fig = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload Excel to start")
