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

team_choice = st.selectbox('Filter on an RSO Team', team)

df = df[df['RSO Team'] == team_choice]
yr1_sum = df.iloc[:,8].sum()
yr2_sum = df.iloc[:,9].sum()
yr3_sum = df.iloc[:,10].sum()
yr4_sum = df.iloc[:,11].sum()

st.dataframe(df, use_container_width = True)

st.write(yr1_sum)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Year1", yr1_sum, delta = None)
col2.metric("Year2", yr2_sum, delta = None)
col3.metric("Year3", yr3_sum, delta = None)
col4.metric("Year4", yr4_sum, delta = None)