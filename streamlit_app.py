import pandas as pd
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.Player} has a :{row.Pos}:")

#st.dataframe(df, use_container_width=True)
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=350, 
    width='100%',
    reload_data=True
)

df = grid_response['data']
selected = grid_response['selected_rows'] 
df2 = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df