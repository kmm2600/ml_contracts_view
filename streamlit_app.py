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
yr1_sum = df.iloc[:,8].sum()
yr2_sum = df.iloc[:,9].sum()
yr3_sum = df.iloc[:,10].sum()
yr4_sum = df.iloc[:,11].sum()
cap = 224800000
yr1_free = cap - yr1_sum
yr2_free = cap - yr2_sum
yr3_free = cap - yr3_sum
yr4_free = cap - yr4_sum
yr1_sumd = "${:,d}".format(yr1_sum)
yr2_sumd = "${:,d}".format(yr2_sum)
yr3_sumd = "${:,d}".format(yr3_sum)
yr4_sumd = "${:,d}".format(yr4_sum)
yr1_freed = "{:,d}".format(yr1_free)
yr2_freed = "{:,d}".format(yr2_free)
yr3_freed = "{:,d}".format(yr3_free)
yr4_freed = "{:,d}".format(yr4_free)

def ufa(cell_value):
    highlight = 'background-color: green;'
    default = ''
    
    if cell_value == 0:
        return highlight
    return default

st.dataframe(df.style.format(thousands=',').applymap(ufa, subset=['2022','2023','2024','2025']), use_container_width = True)
st.caption("You can drag the lower-right corner to re-size the table; green highlighted cells indicate the player is a free agent")

@st.cache
def convert_df(df2):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df2.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download table as CSV",
    data=csv,
    file_name='my_contracts.csv',
    mime='text/csv',
)

st.write("Below are the contract totals by year and cap free space.")
col1, col2, col3 = st.columns(3)
col1.metric(df.columns[9], yr2_sumd, yr2_freed)
col2.metric(df.columns[10], yr3_sumd, yr3_freed)
col3.metric(df.columns[11], yr4_sumd, yr4_freed)

st.caption("Cap free space is based on the 2023 224.8M salary cap and values may be slightly off due to RSO rounding")
st.caption("Green equals free space, red means over the cap")

