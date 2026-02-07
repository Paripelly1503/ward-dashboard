import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(page_title="Ward 26 Voter Search", layout="wide")

st.title("🗳 Ward 26 Voter Search App")
st.write("Enter **House Number / First Name / Last Name** below")

# --------------------------------
# LOAD DATA
# --------------------------------
df_raw = pd.read_excel("26ward.xlsx", header=None)
df_raw.columns = df_raw.iloc[0]
df = df_raw.iloc[1:].copy()

df = df.dropna(how="all")
df = df.fillna("")

df["NAME"] = df.iloc[:,4].astype(str)
df["GENDER"] = df.iloc[:,6].astype(str)
df["AGE"] = df.iloc[:,7].astype(str)
df["HOUSE"] = df.iloc[:,9].astype(str)

# Remove blank name & house
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

# --------------------------------
# SEARCH INPUT (BIG BOX)
# --------------------------------
search = st.text_input(
    "",
    placeholder="🔍 Type Name or House Number and press Enter"
)

st.divider()

# --------------------------------
# SHOW RESULTS ONLY AFTER SEARCH
# --------------------------------
if search:

    results = df[
        df["NAME"].str.contains(search, case=False) |
        df["HOUSE"].str.contains(search, case=False)
    ]

    st.subheader(f"Results Found : {len(results)}")

    st.dataframe(
        results[["NAME","HOUSE","GENDER","AGE"]],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # GENDER PIE
    # -----------------------------
    gender_df = results[results["GENDER"] != ""]
    gender_counts = gender_df["GENDER"].value_counts().reset_index()
    gender_counts.columns = ["Gender","Count"]

    st.subheader("Male vs Female")

    fig = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Start by typing Name or House Number")
