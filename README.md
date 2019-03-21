# Avalanche_db

to make the avalanche data base the code "make_avalanche_db.py" needs to be edited for path names and run.

The paths to files and folders below need to be set.

overview_html =       '/home/damboise/Documents/data_base/html/overview.html'
single_html =  '/home/damboise/Documents/data_base/html/single_avalanche/'
overview_csv  =       '/home/damboise/Documents/data_base/html/overview.csv'
avalanche_map_html = '/home/damboise/Documents/data_base/html/test_map.html'

after that the code is ready to run with python 2.7.

A pop up should open and you should pick what folder the input data is located.


Folium package may make problems.
with anaconda install it with command below
  "conda install -c conda-forge folium "

folium has been added to anacondas base environment to add this base environment to atom use following commands 
"source activate base"
"python -m ipykernel install --user --name base"
