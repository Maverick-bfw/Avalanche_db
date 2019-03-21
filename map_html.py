#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import folium
import numpy as np
from folium.plugins import MarkerCluster
from folium import IFrame
from pyproj import Proj, transform
from overview_tables import make_link_list
#from osgeo import ogr, osr
#
# this code will read the csv data base and show the avalanche events on a html map
#
# Load .csv file
# def find_avalanche_files():
#     pattern = '*.lawinfo' # seek .lawinfo files in the folders
#     myFileList = []
#     for path, subdirs, files in os.walk(root): # find the .lawinfo files and add them to myFileList
#         for fName in files:
#             if fnmatch(fName, pattern):
#                 myFileList.append(os.path.join(path,fName))
#
#     myLinkList = []
#     for fname in myFileList:
#
#         item = single_html +fname.split('/')[-1][:-7]+'html'
#         myLinkList.append(item)
#         return myLinkList

def map_builder(outfile_csv, avalanche_map_html, myLinkList):
    avalDat = pd.read_csv(outfile_csv, sep=';', encoding = 'utf-8')
    # transform coordnates
    lat = []
    lon = []
    coord_list = zip(avalDat['coord_x'],avalDat['coord_y'],avalDat['epsg']) # stitch x , y and epsg in a 3 by X list
                                                                        # ex [(a,b,c),(d,e,f),(g,h,i)...(x,y,z)]
    for coord in coord_list: # loop with our coordnates
#
        if np.isnan(coord[1]):  # checks location coordnate for NaN
            lat.append(47.268891) # if there is no location for the avalanche
            lon.append(11.394561) # It will live in the BFW office

        else:
            try:
                cord_int = int(coord[2]) # changing coord[2] to an int so it is not 31287.0 but 31287 which is required for the projection string
                input_projection_string = 'epsg:%s'%cord_int
                inProj = Proj(init=input_projection_string)
                outProj = Proj(init='epsg:4326')
                x_in,y_in = coord[0], coord[1]
                x_out,y_out = transform(inProj,outProj,x_in,y_in)
                lat.append(y_out)
                lon.append(x_out)
            except: # if something is messed up the avalanche will live at the BFW office
                lat.append(47.268891)
                lon.append(11.394561)

    avalDat['lat']=lat
    avalDat['lon']=lon

    avalDat = avalDat.assign(links = myLinkList) # add html links to data frame before it turns to tuple

    # Neue Karte erstellen 13,436189 47,371885
    m=folium.Map(location=[47.371885,13.436189], zoom_start=7, tiles='Stamen Toner')

    # Add Basemap Tileset (weils so schön is):
    BasemapGrau = folium.TileLayer(tiles=r'https://maps2.wien.gv.at/basemap/bmapgrau/normal/google3857/{z}/{y}/{x}.png',
                                      attr = '<a href=”http://basemap.at” target=”_blank”>basemap.at</a>,\
                                      <a href=”http://creativecommons.org/licenses/by/3.0/at/deed.de”\
                                      target=”_blank”>CC-BY 3.0</a>',
                                      name='Geoland Basemap Grau',overlay=False)


    mCl = MarkerCluster(name='Avalance Data',overlay=True,control=True)

    BasemapOrtho = folium.TileLayer(tiles=r'http://maps2.wien.gv.at/basemap/bmaporthofoto30cm/normal/google3857/{z}/{y}/{x}.jpeg',
                                    attr = 'Datenquelle: <a href="www.basemap.at">basemap.at</a>',
                                    name = 'Basemap Ortho',
                                    overlay = False, control=True)

    BasemapOrtho.add_to(m)
    BasemapGrau.add_to(m)
    # Add Markers with Popups for Avalanche Info-Point Locations
    for row in zip(avalDat['lat'], avalDat['lon'], avalDat['aval_name'], avalDat['wlk_id'], avalDat['projects'],
                   avalDat['mitigation_measures'], avalDat['bool_proc'], avalDat['bool_sim '], avalDat['contact_bfw'], avalDat['links']):
        print row[9]

        html="""
        <a < href="file://%s" onclick="window.open(this.href); return false;" onkeypress="window.open(this.href); return false;" > %s </a> <br>
        <br>
        <b>WLK-ID:</b> %s
        <br>
        <b>Projektbezug: </b> %s
        <br>
        <b>Verbauungen: </b> %s
        <br>
        <b>Processed Data vorhanden: </b> %s
        <br>
        <b>Simulationen vorhanden: </b> %s
        <br>
        <b>Ansprechperson: </b> %s
        <br>
        <a < target="_blank" href="file://%s" > Right click and open link in new tab </a>
        """%(row[9],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        #<a target="_blank" href= "%s" > link to avalanche <a>
        iframe = IFrame(html=html,width=800, height=250)
        popup = folium.Popup(iframe, max_width=2650)

        icon = folium.Icon(icon='glyphicon glyphicon-star',color='blue')
        mCl.add_child(folium.Marker([row[0],row[1]], popup=popup, icon=icon))


    m.add_child(mCl)
    m.add_child(folium.LayerControl())
    #m
    m.save(avalanche_map_html)



if __name__ == "__main__":

    overview_html =       '/home/damboise/Documents/data_base/html/overview.html'
    single_html =  '/home/damboise/Documents/data_base/html/single_avalanche/'
    outfile_csv  =       '/home/damboise/Documents/data_base/html/overview.csv'
    #avalanche_map_html = '/home/P/Projekte/xxxxx_Lawinendaten/html/Lawinendaten.html'
    avalanche_map_html = '/home/damboise/Documents/data_base/html/test_map.html'


    print "Hi chief what folder should I scan"
   #root = tkFD.askdirectory() # this should be the folder that contains the folders on individual avalanche data
    root = '/home/damboise/Documents/data_base/test_data'
    print "searching", root
    myFileList, myLinkList = make_link_list(root, single_html)
    map_builder(outfile_csv, avalanche_map_html, myLinkList)
