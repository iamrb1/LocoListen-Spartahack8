import streamlit as st
import json
import requests
import datetime
from gsheetsdb import connect


# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet1 = st.secrets['Sheet1']
sheet2 = st.secrets['Sheet2']
sheet3 = st.secrets['Sheet3']
sheet4 = st.secrets['Sheet4']
sheet5 = st.secrets['Sheet5']
sheet6 = st.secrets['Sheet6']
sheet7 = st.secrets['Sheet7']
sheet8 = st.secrets['Sheet8']
rows = run_query(f'SELECT * FROM "{sheet1}"')

# Print results

response = requests.get("http://ip-api.com/json")
data = json.loads(response.text)
st.write("City: ", data["city"])
st.write("Region: ", data["regionName"])
st.write("Country: ", data["country"])
st.write("Latitude: ", data["lat"])
st.write("Longitude: ", data["lon"])
