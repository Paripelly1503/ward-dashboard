import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward 26 Voter Dashboard", layout="wide")
st.title("🗳 Ward 26 Voter Dashboard")

# -----------------------------
# LOAD FILE AUTOMATICALLY
# -----------------------------
df_raw = pd.read_excel("26ward.xlsx", header=None)

df_raw.columns = df_raw.iloc[0]
df = df_raw.iloc[1:].copy()

# Remove empty rows
df = df.dropna(how="all")
df = df.fillna("")

# Map required columns
df["NAME"] = df.iloc[:,4].astype(str)
df["GENDER"] = df.iloc[:,6].astype(str)
df["AGE"] = df.iloc[:,7].astype(str)
df["HOUSE"] = df.iloc[:,9].astype(str)

# Remove blank NAME and HOUSE rows
df = df[(df["NAME"].str.strip() != "") & (df["HOUSE"].str.strip() != "")]

# Clean gender
def clean_gender(x):
    x = x.strip().upper()
    if x == "M":
        return "Male"
    elif x == "F":
        return "Female"
    else:
        return ""

df["GENDER"] = df["GENDER"].apply(clean_gender)

# -----------------------------
# SEARCH BOX
# -----------------------------
st.sidebar.header("Search")
search = st.sidebar.text_input("Type Name or House Number")

filtered = df.copy()

if search:
    filtered = filtered[
        df["NAME"].str.contains(search, case=False) |
        df["HOUSE"].str.contains(search, case=False)
    ]

# -----------------------------
# METRICS
# -----------------------------
c1, c2 = st.columns(2)
c1.metric("Members Found", len(filtered))
c2.metric("Total Houses", filtered["HOUSE"].nunique())

st.divider()

# -----------------------------
# TABLE
# -----------------------------
st.subheader("Members List")
st.dataframe(
    filtered[["NAME","HOUSE","GENDER","AGE"]],
    use_container_width=True
)

st.divider()

# -----------------------------
# GENDER PIE
# -----------------------------
gender_df = filtered[filtered["GENDER"] != ""]
gender_counts = gender_df["GENDER"].value_counts().reset_index()
gender_counts.columns = ["Gender","Count"]

st.subheader("Male vs Female")
fig = px.pie(gender_counts, names="Gender", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)
