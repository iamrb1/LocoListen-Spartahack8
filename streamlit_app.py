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

rows = run_query(f'SELECT * FROM "{sheet1}"')

# Print results

response = requests.get("http://ip-api.com/json")
data = json.loads(response.text)
st.write("City: ", data["city"])
st.write("Region: ", data["regionName"])
st.write("Country: ", data["country"])
st.write("Latitude: ", data["lat"])
st.write("Longitude: ", data["lon"])
