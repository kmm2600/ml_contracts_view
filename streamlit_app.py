import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="RSO Contract Viewer",
    layout="wide"
)

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

st.title(f"RSO Team Contract Viewer")

team = sorted(list(df['RSO Team'].drop_duplicates()))
curr_yr = df.columns[9]
team_choice = st.selectbox('Filter on an RSO Team', team)

st.write("The table below shows all players under contract in ", curr_yr, ". You can sort the table by clicking on a column header.")
df = df[df['RSO Team'] == team_choice]
df = df[df.iloc[:,9] > 0]
yr1_sum = "${:,d}".format(df.iloc[:,8].sum())
yr2_sum = "${:,d}".format(df.iloc[:,9].sum())
yr3_sum = "${:,d}".format(df.iloc[:,10].sum())
yr4_sum = "${:,d}".format(df.iloc[:,11].sum())

st.dataframe(df, use_container_width = True)
st.caption("You can drag the lower-right corner to re-size the table")

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(my_large_df)

st.download_button(
    label="Download table as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

st.write("Below are the contracts totals by year")
col1, col2, col3 = st.columns(3)
col1.metric(df.columns[9], yr2_sum, delta = None)
col2.metric(df.columns[10], yr3_sum, delta = None)
col3.metric(df.columns[11], yr4_sum, delta = None)

