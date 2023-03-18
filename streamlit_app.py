import pandas as pd
import streamlit as st
import numpy as np

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

st.title(f"RSO Team Contract Viewer")

team = list(df['RSO Team'].drop_duplicates())
curr_yr = df.columns[9]
team_choice = st.selectbox('Filter on an RSO Team', team)

st.subheader("The table below shows all players under contract in ", curr_yr)
df = df[df['RSO Team'] == team_choice]
df = df[df.iloc[:,9] > 0]
yr1_sum = "${:,d}".format(df.iloc[:,8].sum())
yr2_sum = "${:,d}".format(df.iloc[:,9].sum())
yr3_sum = "${:,d}".format(df.iloc[:,10].sum())
yr4_sum = "${:,d}".format(df.iloc[:,11].sum())

st.dataframe(df, use_container_width = True)
st.caption("You can drag the lower-right corner to re-size the table")
st.subheader("Below are the contracts totals by year")
col1, col2, col3 = st.columns(3)
col1.metric(df.columns[9], yr2_sum, delta = None)
col2.metric(df.columns[10], yr3_sum, delta = None)
col3.metric(df.columns[11], yr4_sum, delta = None)
