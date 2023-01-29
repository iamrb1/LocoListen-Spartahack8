import streamlit as st
import json
import requests




response = requests.get("http://ip-api.com/json")
data = json.loads(response.text)
st.write("City: ", data["city"])
st.write("Region: ", data["regionName"])
st.write("Country: ", data["country"])
st.write("Latitude: ", data["lat"])
st.write("Longitude: ", data["lon"])
