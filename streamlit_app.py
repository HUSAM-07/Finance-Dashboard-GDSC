import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Read Google Sheets URL from secrets.toml
gsheets_url = st.secrets["connections"]["gsheets"]["spreadsheet"]

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read()

# Function to filter data based on user input
def filter_data(data, filters):
    filtered_data = data.copy()
    for column, value in filters.items():
        if value:
            filtered_data = filtered_data[filtered_data[column].str.contains(value)]
    return filtered_data

# Streamlit app layout
st.title('Google Sheets Data Viewer and Editor')
st.sidebar.header('Filters')

# Display filters
filter_columns = list(data[0].keys()) if data else []
filters = {}
for column in filter_columns:
    filters[column] = st.sidebar.text_input(column, '')

filtered_data = filter_data(data, filters)

# Display filtered data
st.write('Filtered Data:')
st.write(filtered_data)

# Data update section
st.header('Update Data')

# Select row to update
row_index = st.number_input('Row index to update:', min_value=0, max_value=len(filtered_data)-1, step=1)

if st.button('Update Row'):
    if row_index < len(filtered_data):
        for column in filtered_data.columns:
            new_value = st.text_input(f'New value for {column}:', value=filtered_data.iloc[row_index][column])
            filtered_data.at[row_index, column] = new_value
        st.write('Row updated successfully!')
    else:
        st.write('Row index is out of range.')

# Save updated data to Google Sheets
# You can use Google Sheets API to save the updated data back to Google Sheets

# Display updated data
st.write('Updated Data:')
st.write(filtered_data)
