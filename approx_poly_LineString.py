# This file converts a LineString shapefile to a single polygon shape
# using the convex hull
# functions of the Shapely library.
# A map of districts of Maharashtra is used for this example.
import matplotlib.pyplot as plt
import geopandas
from geopandas import GeoSeries
from shapely.geometry import Polygon,Point,MultiLineString
g=geopandas.read_file("maharashtra/maharashtra_administrative.shp")
g.plot()
boundary=[]
for district in g["geometry"]:
    boundary.append(district)
boundary_poly=MultiLineString(boundary).convex_hull
area=GeoSeries(boundary_poly)
area.plot()
plt.show()