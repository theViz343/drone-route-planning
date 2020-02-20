#! /bin/bash 
echo "Please wait. This may take several minutes..."
python3 -m venv venv
source venv/bin/activate
pip3 install shapely
pip3 install geopandas
pip3 install matplotlib
deactivate
