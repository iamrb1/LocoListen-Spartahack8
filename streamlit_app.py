import streamlit as st
import folium

@st.cache
def create_map():
    m = folium.Map()
    folium.Marker(
        location=[45.523, -122.675],
        popup='Portland, OR',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    return m

map_ = create_map()

if st.button("Hover over me!"):
    map_.add_child(folium.Popup("Hovering!"))

st.write(map_)
