import os
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd







m = leafmap.Map(tiles="stamentoner")

def addAttributesOptions(gfile):
    atts = gfile.columns
    tuAtts = tuple(" ")+tuple(atts)
    attList = st.selectbox("choose the value column",tuAtts)
    if not attList == " ":
        lat = gfile.geometry.y
        long = gfile.geometry.x
        value = gfile[attList]
        st.write(value)
        length = len(lat)
        data = []
        for i in range(0,length):
            point = [lat[i],long[i],float(value[i])]
            data.append(point)
        st.write(data)

        m.add_heatmap(data)
        

with st.sidebar:
    st.markdown("<h1 style='color: aqua; text-align: center;'>AS MAP</h1>",unsafe_allow_html=True)
    baseList = st.selectbox("Choose your Basemap",('Open Street Map',"stamentoner",'Google HYBRID','Esri NatGeoWorld'))
    if baseList == "Open Street Map":
        pass         
    elif baseList == "stamentoner":
        st.write("iam here")
        m.add_basemap(tiles="stamentoner")
    elif  baseList == "Google HYBRID":
        m.add_basemap("HYBRID")
    elif baseList == 'Esri NatGeoWorld':
        m.add_basemap("Esri.NatGeoWorldMap")
    heatFile = st.file_uploader("upload file for heat map",type="geojson")
    if heatFile:
        gfile = gpd.read_file(heatFile)
        if  gfile.crs == 3857:
            gfile = gfile.to_crs(4326)
            st.write(gfile.geometry)
        addAttributesOptions(gfile)
        m.add_gdf(gfile)


m.to_streamlit(width=1000,height=700)
