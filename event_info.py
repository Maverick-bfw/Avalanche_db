#!/usr/bin/python
# -*- coding: utf-8 -*-
# Avalanche data base builder
# laden der benoetigten libraries
import os
import codecs
from fnmatch import fnmatch
import tkFileDialog as tkFD



def avalanche_event_to_html(root, outfile_html, outfile_csv):
    

    pattern = '*.lawinfo' # seek .lawinfo files in the folders

    myLawinfoList = []
    myHtmlList = []
    #myCssList = []
    for path, subdirs, files in os.walk(root):
        for fName in files:
             if fnmatch(fName, pattern):
                myLawinfoList.append(os.path.join(path,fName))

    for fname in myLawinfoList:
        myHtmlList.append(outfile_html+fname.split('/')[-1][:-7]+'html')

    myDicList = []

    for file in myLawinfoList:
        myDict = {}
        myAddInfo = []
        #myFile = codecs.open(file, 'r', 'ISO-8859-1')
        myFile = open(file, 'r')
        flag = 0

        for aline in myFile :
            if 'ADDITIONAL META-DATA' in aline:
                flag = 1
            if aline != "\n"  and aline.split('#')[0].split(':')[0] and flag == 0:
                itemName = aline.split('#')[0].split(':')[0]
                item     = aline.split('#')[0].split(':')[1].strip() #.decode('string-escape').decode("utf-8")
                myDict[itemName] = item
            if flag == 1:
                if aline[0] == '#':
                    pass
                else:
                    myAddInfo.append(aline.rstrip())

        myDict['addInfo']=myAddInfo

        myDicList.append(myDict)

    htmlStringList = []
    for item in myDicList:


        htmlString0 = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
          <meta http-equiv="content-type" content="text/html; charset="utf-8" />
          <link href="txtstyle.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
        <h1>MetaInfo %s</h1>
        <hr>
        <p>
        <b>MANDATORY META-DATA:</b>
        </p>
        <p>
        """%item['aval_name']
        htmlString1 = """</p>
        <p>
        <b>ADDITIONAL META-DATA:</b>"""

        htmlString2 = """</p></body></html>"""

        myhtmlString = ''
        mandatoryTable = ''
        mandatoryTable += """<table>
    <tr class='grey'><td><b>aval_name:</b></td><td>%s</td></tr>
    <tr><td><b>POI_x:</b></td><td>%s</td></tr>
    <tr class='grey'><td><b>POI_y:</b></td><td>%s</td></tr>
    <tr><td><b>epsg:</b></td><td>%s</td></tr>
    <tr class='grey'><td><b>wlk_id:</b></td><td>%s</td></tr>
    <tr><td><b>mitigation_measures:</b></td><td>%s</td></tr>
    <tr class='grey'><td><b>projects:</b></td><td>%s</td></tr>
    <tr><td><b>bool_processed:</b></td><td>%s</td></tr>
    <tr class='grey'><td><b>bool_sim:</b></td><td>%s</td></tr>
    <tr><td><b>contact_bfw:</b></td><td>%s</td></tr>
    </table>"""%(item['aval_name'],item['POI_x'],item['POI_y'],item['epsg'],
                item['wlk_id'],item['mitigation_measures'],item['projects'],
                item['bool_processed'],item['bool_sim'],item['contact_bfw'])
        additionalInfo = ''
        for line in item['addInfo']:
            additionalInfo += '<br>'+line
        myhtmlString = myhtmlString + htmlString0 + mandatoryTable + htmlString1 + additionalInfo + htmlString2
        htmlStringList.append(myhtmlString)


#makes individual html files for every avalanche
        for string, fNameHtml in zip(htmlStringList, myHtmlList):
            outFile = open(fNameHtml,'w')
            outFile.write(string)
            outFile.close()
            
            
            

