
import requests
from gsheetsdb import connect



import streamlit as st
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
import numpy as np



import json

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

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO https://docs.google.com/spreadsheets/d/1M-dpek_BEXoHUUagSiZwiMm8KQ_R-fIquiytL_AboRU/edit#gid=0(name,priority,status_id,project_id,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''





    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def upload(lat, lon):
    roundedLongitude = round((lon) / 10) * 10
    if(lat >= 25):
        dataBaseToWriteTo = str(twentyfiveLatDict[roundedLongitude])
    else:
        dataBaseToWriteTo = str(zeroLatDict[roundedLongitude])


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
    130: sheet1,
120: sheet1,
110: sheet2,
100: sheet3,
90: sheet3,
80: sheet4,
70: sheet4,
60: sheet4
}

zeroLatDict = {
    130: sheet1,
    120: sheet1,
    110: sheet2,
    100: sheet3,
    90: sheet3,
    80: sheet4,
    70: sheet4,
    60: sheet4

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
    matrix=Get_Top_10_10(currentLat,currentLong,sheet1)
    dataBaseToWriteTo=twentyfiveLatDict[newlongitude]
else:
    matrix = Get_Top_10_10(currentLat, currentLong,
                           sheet1)
    dataBaseToWriteTo=zeroLatDict[newlongitude]


type ='song'
newSongLink = 'https://open.spotify.com/track/3ODXRUPL44f04cCacwiCLC?si=e794949cf4a94b0a'
newPlaylistLink = ''


#newRow=(currentLat,currentLong,newSongLink,type)


#create_task(conn,newRow)


songMatrix=[]
playlistMatrix=[]
completeMatrix=[[currentLat,currentLong]]




for key, value in matrix.items():
    if key=='song':
        for song in value:
            thingg=[song.Lat,song.Lon]
            thinggg=[song.Link]
            songMatrix.append(thinggg)
            completeMatrix.append(thingg)
    else:
        for playlist in value:
            thinggg = [playlist.Link]
            thingg=[playlist.Lat,playlist.Lon]
            playlistMatrix.append(thinggg)
            completeMatrix.append(thingg)




st.write("City: ", data["city"])
st.write("Region: ", data["regionName"])
st.write("Country: ", data["country"])
st.write("Latitude: ", data["lat"])
st.write("Longitude: ", data["lon"])



#Title
st.markdown(""" <style> .font {
font-size:50px ; font-family: 'Gotham'; color: rgb(30, 215, 96);} 
</style> """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: rgb(30, 215, 96);'>LocoListen</h1>", unsafe_allow_html = True)

#Alignment of Logo
col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    pass
with col7:
    pass
with col9:
    pass
with col10:
    pass
with col8:
    st.image("https://media.giphy.com/media/yOCHlNTlbpO9nrUCuD/giphy.gif", width=130,)

#Site-wide font and color css changes
st.markdown(""" <style> .font {
font-size:50px ; font-family: 'Gotham'; color: rgb(30, 215, 96);} 
</style> """, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: rgb(30, 215, 96);'>Find what your community is listening to!</h3>", unsafe_allow_html = True)

#Map creation
df = pd.DataFrame(
    completeMatrix,
    columns=['lat', 'lon'])

st.map(df)

#centering buttons
col1, col2, col3 , col4, col5 = st.columns(5)
m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(30, 215, 96);
        }
        </style""", unsafe_allow_html = True)
with col1:
    button1 = st.button("Upload Playlists")
    if button1:
        user_textt = st.text_input("Enter Playlist URL:")


        if len(user_textt) > 0:
            st.markdown(""" <style> .font {
                        font-size:50px ; font-family: 'Gotham'; color: white;} 
                        </style> """, unsafe_allow_html=True)
            st.write("Upload Success!")
with col2:
    button2 = st.button("Upload Songs by you!")
    if button2:
        user_text = st.text_input("Enter Song URL:")
        if len(user_text) > 0:
            st.markdown(""" <style> .font {
                        font-size:50px ; font-family: 'Gotham'; color: white;} 
                        </style> """, unsafe_allow_html=True)
            st.write("Upload Success!")


with col4:
    button4 = st.button("View Songs near you!")
    if button4:
        df3 = pd.DataFrame(
            songMatrix,
            columns=['Songs'])
            #list for songs
        st.dataframe(df3)
with col5:
    button5 = st.button("About Need Sleep Inc.!")
    if button5:
        st.markdown(""" <style> .font {
        font-size:50px ; font-family: 'Gotham'; color: white;} 
        </style> """, unsafe_allow_html=True)
        st.markdown(':white[_Need Sleep Inc. is a team of student programmers from Michigan State University._]')
        st.write("\n")
        st.markdown(':white[_This is a project developed during Spartahack 8._]')

with col3:
    button3 = st.button("View Playlists near you!")
    if button3:
        df2 = pd.DataFrame(
            playlistMatrix,
            columns=['Playlist'])

        st.dataframe(df2)

#footer code css
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: rgb(30, 215, 96);
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;'  target="_blank">Need Sleep Inc. ©2023 </a></p>
</div>
"""


st.markdown(footer,unsafe_allow_html=True)
