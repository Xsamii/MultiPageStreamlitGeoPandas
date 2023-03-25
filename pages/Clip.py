import os
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd


clippedFeat=None
isClipped = False

def clipFun (sourceFile,clipFile):
        
        if sourceFile:
             gsourceFile = gpd.read_file(sourceFile)
        else :
             st.warning("please enter the source file")
             return
        if clipFile:
             gclipFile = gpd.read_file(clipFile)
        else:
             st.warning("please enter Clip File")
             return
        global clippedFeat
        clippedFeat = gsourceFile.clip(gclipFile)
        global isClipped
        isClipped = True
        





with st.form("Clip Form") as clipForm:

    col1,col2 = st.columns(2)

    col1.subheader("Upload the Source File")
    col2.subheader("Upload the Clip File")

    sourceFile= col1.file_uploader("s")
    clipFile= col2.file_uploader("c")

    submitted  = st.form_submit_button("Clip")
    if submitted :
        clipFun(sourceFile,clipFile)

if isClipped:
    newFileName = st.text_input("enter file name")
    clippedFeat.to_file(f'cash/{newFileName}.geojson', driver='GeoJSON')
    st.download_button(
                label="Download clipped file as geojson",
                data=f'cash/{newFileName}.json',
                file_name=f'{newFileName}.geojson',
            )
addMap = st.button("Show Clipped Layer on map")
if addMap and clippedFeat:
     m = leafmap.Map()
     m.add_gdf(clippedFeat)
     m.to_streamlit(width=1000,height=700)
