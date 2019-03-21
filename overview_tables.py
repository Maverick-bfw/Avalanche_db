#!/usr/bin/python
# -*- coding: utf-8 -*-
# Avalanche data base builder
# laden der benoetigten libraries
import os
import codecs
from fnmatch import fnmatch
import tkFileDialog as tkFD



def make_link_list(root, single_html):
    pattern = '*.lawinfo' # seek .lawinfo files in the folders
    myFileList = []
    for path, subdirs, files in os.walk(root): # find the .lawinfo files and add them to myFileList
        for fName in files:
            if fnmatch(fName, pattern):
                myFileList.append(os.path.join(path, fName))


    myLinkList = []
    for fname in myFileList:
        #item = '/home/P/Projekte/xxxxx_Lawinendaten/html/singlehtmls/'+fname.split('/')[-1][:-7]+'html'
        #item = '/home/simulation/avalanche_data/html/singlehtmls/'+fname.split('/')[-1][:-7]+'html'
        #item = '/home/simulation/avalanche_data/00_data_scripts/html/singlehtmls/'+fname.split('/')[-1][:-7]+'html'
        item = single_html +fname.split('/')[-1][:-7]+'html'
        myLinkList.append(item)

    print "I found ", len(myLinkList), "files"
    return myFileList, myLinkList

def overview_csv_html(root, single_html, outfile_html, outfile_csv, myFileList, myLinkList):
    myDicList = []
    for file in myFileList:
        myDict = {}
        myFile = open(file, 'r')

        for aline in myFile :
            if 'ADDITIONAL META-DATA' in aline: # == "######### ADDITIONAL META-DATA #######################\n":  # ''Alle Plichtfelder'' vor # Additional INFO\n mussen ausgefullt sein !!!a
                break
            if aline != "\n"  and aline.split('#')[0].split(':')[0]:
                itemName = aline.split('#')[0].split(':')[0]
                item     = aline.split('#')[0].split(':')[1].strip() #.decode('string-escape').decode("utf-8")
                myDict[itemName] = item

        myDicList.append(myDict)


        # 1) open text-file
        # myDic = {}
        # 2) read file to dictionary --> {'dataset': 'dataset 1', 'description': 'blablba',
        #                             'lat': 46.12213, 'lon': 11.9834, 'all Other items': 'blabla'}
        # myDictList.append(dictionary)

    # 3) open html-file
    # 4) suche nach der Tabelle (alles zwischen <tbody> und </tbody>)
    # 5) losche den teil aus der html-file

    # for dic in myDicList:
        # 6) schreibe in html file:
        """
        <tr>
            <td> dict_item 1 </td>
            <td> dict_item 2 </td>
            <td> etc ... </td>
        </tr>
        """
    myTableElements = ''
    for item, link in zip(myDicList, myLinkList):
        myTableElements = myTableElements + '<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td><td><a target="_blank" href="%s">link</a></td>\n'%(item['aval_name'],
        item['wlk_id'],
        item['projects'],
        item['contact_bfw'],
        item['mitigation_measures'],
        item['bool_processed'],
        item['bool_sim'],
        item['POI_x']+' '+item['POI_y'],
        item['epsg'],
        link)
        myTableElements = myTableElements + '</tr>\n'

    bla1 = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html>
    <head>
      <meta http-equiv="content-type" content="text/html; charset=utf-8" />
      <link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.10.5/css/jquery.dataTables.css">
    </head>
    <body>
    <CENTER>
      <h1>Übersicht Lawinendaten Abt. 6-1</h1>
    </CENTER>
    <hr>
    <p></p>
    <hr>

    <table id="example" class="display compact" width="90%" cellspacing="0">
        <thead>
          <tr>
            <th>Dataset</th>
            <th>WLK_ID</th>
            <th>Projects</th>
            <th>Contact BFW</th>
            <th>Mitigation Measures</th>
            <th>Processed Data</th>
            <th>Simulation Data</th>
            <th>Location</th>
            <th>EPSG</th>
            <th>further Info</th>
          </tr>
        </thead>
        <tfoot>
          <tr>
            <th>Dataset</th>
            <th>WLK_ID</th>
            <th>Projects</th>
            <th>Contact BFW</th>
            <th>Mitigation Measures</th>
            <th>Processed Data</th>
            <th>Simulation Data</th>
            <th>Location</th>
            <th>EPSG</th>
            <th>further Info</th>
          </tr>
        </tfoot>

        <tbody class="list"> """

    bla2 = """<!-- Hier kommt die Info aus den .txt files rein -->

        </tbody>
      </table>
    <!--<script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.2.min.js"></script>
      <script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.10.5/jquery.dataTables.min.js"></script> -->
      <!-- this should work without Internet Access -->
      <script type="text/javascript" charset="utf8" src="./dependencies/jquery-1.8.2.min.js"></script>
      <script type="text/javascript" charset="utf8" src="./dependencies/jquery.dataTables.min.js"></script>

      <script>
      $(function(){
          $('#example').dataTable( {
            responsive: true,
            sPaginationType: "full_numbers",
            initComplete: function () {
                var api = this.api();

                api.columns().indexes().flatten().each( function ( i ) {
                    var column = api.column( i );
                    var select = $('<select><option value=""></option></select>')
                        .appendTo( $(column.footer()).empty() )
                        .on( 'change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );

                            column
                                .search( val ? '^'+val+'$' : '', true, false )
                                .draw();
                        } );

                    column.data().unique().sort().each( function ( d, j ) {
                        select.append( '<option value="'+d+'">'+d+'</option>' )
                    } );
                } );
            }
        } );
        $('#example').dataTable().columnFilter();
      });
      </script>

    </body>
    </html>"""
    outFile = open(outfile_html,'w')
    outFile.write(bla1+myTableElements+bla2)
    outFile.close()


    outfile = open(outfile_csv, 'w')

    outfile.write('aval_name;coord_x;coord_y;epsg;wlk_id;contact_bfw;projects;mitigation_measures;bool_proc;bool_sim \n')
    for item in myDicList:
        outfile.write(item['aval_name']+';')
        outfile.write(item['POI_x']+';')
        outfile.write(item['POI_y']+';')
        outfile.write(item['epsg']+';')
        outfile.write(item['wlk_id']+';')
        outfile.write(item['contact_bfw']+';')
        outfile.write(item['projects']+';')
        outfile.write(item['mitigation_measures']+';')
        outfile.write(item['bool_processed']+';')
        outfile.write(item['bool_sim']+'\n')

    outfile.close()



############ only useful to run stand alone not used with make_avalanche_db.py########################
if __name__ == "__main__":

    overview_html = '/home/damboise/Documents/data_base/html/overview.html'
    single_html = '/home/damboise/Documents/data_base/html/single_avalanche/'
    overview_csv  = '/home/damboise/Documents/data_base/html/overview.csv'
    #avalanche_map_html = '/home/P/Projekte/xxxxx_Lawinendaten/html/Lawinendaten.html'
    avalanche_map_html = '/home/damboise/Documents/data_base/html/test_map.html'


    print "Hi chief what folder should I scan"
    #root = tkFD.askdirectory() # this should be the folder that contains the folders on individual avalanche data
    root = '/home/damboise/Documents/data_base/test_data'
    print "searching", root
    myFileList, myLinkList = make_link_list(root, single_html)
    overview_csv_html(root, single_html, overview_html, overview_csv, myFileList, myLinkList)
  #  event_info.avalanche_event_to_html(root, single_html, overview_csv)
 #   map_html.map_builder(overview_csv, avalanche_map_html)
