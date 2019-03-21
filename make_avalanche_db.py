import overview_tables
import event_info
import map_html
import tkFileDialog as tkFD
import os
import codecs
from fnmatch import fnmatch


if __name__ == "__main__":

    overview_html =       '/home/damboise/Documents/data_base/html/overview.html'
    single_html =  '/home/damboise/Documents/data_base/html/single_avalanche/'
    overview_csv  =       '/home/damboise/Documents/data_base/html/overview.csv'
    avalanche_map_html = '/home/damboise/Documents/data_base/html/test_map.html'


    print "Hi chief what folder should I scan"
    #root = tkFD.askdirectory() # this should be the folder that contains the folders on individual avalanche data
    root = '/home/damboise/Documents/data_base/test_data'
    print "searching", root

    html_links = overview_tables.overview_csv_html(root, single_html, overview_html, overview_csv)
    event_info.avalanche_event_to_html(root, single_html, overview_csv)
    map_html.map_builder(overview_csv, avalanche_map_html, html_links)
    print "All done! Outputs can be found in " , single_html
    print "Have a nice day :)"
