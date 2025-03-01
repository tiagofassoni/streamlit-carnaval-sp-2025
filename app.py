import streamlit as st
import json
import pandas as pd
from datetime import datetime

def load_data():
    with open('actual_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    blocks = []
    for entry in data:
        block = {
            'name': entry['fields']['name'],
            'date': pd.to_datetime(entry['fields']['startDate']).strftime('%Y-%m-%d'),
            'time': pd.to_datetime(entry['fields']['startDate']).strftime('%H:%M'),
            'address': entry['fields']['address'],
            'neighborhood': entry['fields']['neighborhood'],
            'estimated_audience': entry['fields']['estimatedAudience'],
            'instagram': entry['fields']['instagramLink']
        }
        blocks.append(block)
    
    return pd.DataFrame(blocks)

# App title
st.title('São Paulo Carnival Blocks 2025')

# Load data
df = load_data()

# Date filter
available_dates = sorted(df['date'].unique())
selected_date = st.selectbox('Select date', ['All dates'] + available_dates)

# Search box
search = st.text_input('Search blocks by name')

# Apply filters
filtered_df = df.copy()
if selected_date != 'All dates':
    filtered_df = filtered_df[filtered_df['date'] == selected_date]
if search:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False)]

# Display the table
st.dataframe(
    filtered_df,
    column_config={
        'name': 'Block Name',
        'date': 'Date',
        'time': 'Start Time',
        'address': 'Address',
        'neighborhood': 'Neighborhood',
        'estimated_audience': 'Est. Audience',
        'instagram': st.column_config.LinkColumn('Instagram')
    },
    hide_index=True
)

# Show total blocks found
st.write(f'Total blocks found: {len(filtered_df)}')