import os
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd


newFileName = None

def changeFileFormat(gdf,targetFormat,fileName):
    if targetFormat == "geopackage":
         layeName = st.text_input("Enter layer name")
         gdf.to_file(f'cash/{fileName}.gpkg', driver='GPKG', layer=f'{layeName}')
         global newFileName
         newFileName= f'cash/{fileName}.gpkg'
         return True
    if targetFormat == "shapefile":
        gdf.to_file(f'cash/{fileName}.shp') 
        newFileName =f'cash/{fileName}.shp'
        return True  
    if targetFormat == "geojson":
        gdf.to_file(f'cash/{fileName}.geojson', driver='GeoJSON')
        newFileName = f'cash/{fileName}.geojson'
        return True
    elif targetFormat == "parquet":
        gdf.to_parquet(f'cash/{fileName}.parquet') 
        newFileName = f'cash/{fileName}.parquet'
        return True
    elif targetFormat ==  "feather":
        gdf.to_feather(f'cash/{fileName}.feather')
        newFileName = f'cash/{fileName}.feather'
        return True

file= st.file_uploader("upload the Source File")
if file :
        fileName = file.name.split('.')
        ext = fileName[1]
        if ext == "parquet":
             gfile = gpd.read_parquet(file)
        elif ext == "feather":
             gfile = gpd.read_feather(file) 
        else:
            gfile = gpd.read_file(file)
        st.header("the file format is "+ext)
        with  st.form("Parameters") as changeFormatForm:
            targetFormat = st.selectbox("Target Format",("geojson","parquet","feather","shapefile","geopackage"))
            fileName = st.text_input("Enter New File Name")
            submitted  = st.form_submit_button("change file format")
            if submitted :
                changeFileFormat(gfile,targetFormat,fileName)


if newFileName:
    st.download_button(
                    label="Download file",
                    data=newFileName,
                    file_name=f'{fileName}.{targetFormat}',
                )
        





    




# with st.sidebar:
    # st.markdown("<h1 style='color: aqua; text-align: center;'>AS MAP</h1>",unsafe_allow_html=True)
    # baseList = st.selectbox("Choose your Basemap",('Open Street Map',"stamentoner",'Google HYBRID','Esri NatGeoWorld'))
    # if baseList == "Open Street Map":
    #     pass         
    # elif baseList == "stamentoner":
    #     st.write("iam here")
    #     m.add_basemap(tiles="stamentoner")
    # elif  baseList == "Google HYBRID":
    #     m.add_basemap("HYBRID")
    # elif baseList == 'Esri NatGeoWorld':
    #     m.add_basemap("Esri.NatGeoWorldMap")

    

# m.to_streamlit(width=1000,height=700)
