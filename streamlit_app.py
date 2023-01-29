import streamlit as st
import json
import requests
import datetime
from gsheetsdb import connect


class Song:
    Lat=0
    Lon=0
    Link=0

    def __init__(self,lat,long,link):
        self.Lat=lat
        self.Lon=long
        self.Link=link


class Playlist:
    Lat = 0
    Lon = 0
    Link = 0

    def __init__(self, lat, long, link):
        self.Lat = lat
        self.Lon = long
        self.Link = link

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def Get_Top_10_10(currentLat,currentLong,sheet):

    nearMusic = {'Song': [], 'Playlist': []}

    rows = run_query(f'SELECT * FROM "{sheet}"')

    for row in rows:
        if (currentLat > float(row.Latitude) + 5 and currentLat < float(
                row.Latitude) - 5) or (
                currentLong > float(row.Longitude) + 5 and currentLong < float(
                row.Longitude) - 5):
            continue
        if row.Type=='song':

            song=Song(row.Latitude,row.Longitude,row.Link)
            nearMusic['Song'].append(song)
        if row.Type=='playlist':
            playlist=Playlist(row.Latitude,row.Longitude,row.Link)
            nearMusic['Playlist'].append(playlist)
        if len(nearMusic['Song'])==10 and len(nearMusic['Playlist'])==10:
            break
    return nearMusic







# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.



sheet1 = st.secrets['Sheet1']
sheet2 = st.secrets['Sheet2']
sheet3 = st.secrets['Sheet3']
sheet4 = st.secrets['Sheet4']
sheet5 = st.secrets['Sheet5']
sheet6 = st.secrets['Sheet6']
sheet7 = st.secrets['Sheet7']
sheet8 = st.secrets['Sheet8']

twentyfiveLatDict = {
    0: sheet1,
    10: sheet2,
    20: sheet3,
    30: sheet4,
    80: sheet4
}

zeroLatDict = {
    0: sheet5,
    10: sheet6,
    20: sheet7,
    30: sheet8,
    40: sheet8
}

# Retrieve Location via IP
response = requests.get("http://ip-api.com/json")
data = json.loads(response.text)
#currentLat=36
#currentLong=0

currentLat=float(data["lat"])
currentLong=float(data["lon"])

newlongitude = round((currentLong * -1) / 10) * 10

if(currentLat >= 25):
    matrix=Get_Top_10_10(currentLat,currentLong,twentyfiveLatDict[newlongitude])
else:
    matrix = Get_Top_10_10(currentLat, currentLong,
                           zeroLatDict[newlongitude])



for key, value in matrix.items():
    st.write(key)
    for i in value:

        st.write(i.Link,i.Lat,i.Lon)



st.write("City: ", data["city"])
st.write("Region: ", data["regionName"])
st.write("Country: ", data["country"])
st.write("Latitude: ", data["lat"])
st.write("Longitude: ", data["lon"])
