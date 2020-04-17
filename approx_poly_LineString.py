# This file converts a LineString shapefile to a single polygon shape
# using the convex hull
# functions of the Shapely library.
# A map of districts of Maharashtra is used for this example.
from math import ceil
import matplotlib.pyplot as plt
import geopandas
import matplotlib.patches as patches
from geopandas import GeoSeries
from shapely.geometry import Polygon,Point,MultiLineString

g=geopandas.read_file("maharashtra/maharashtra_administrative.shp")
# Three subplots showing different Info
fig,ax=plt.subplots(2,2)

g.plot(ax=ax[0][0])    # Plot shapefile info directly

# Calculate the Convex Hull of all MultiLineString districts
boundary=[]
for district in g["geometry"]:
    boundary.append(district)
boundary_poly=MultiLineString(boundary).convex_hull
area=GeoSeries(boundary_poly)

# Calculation of points with set width between them
width=1
offset=width/2
x0=area.bounds["minx"][0]
x1=area.bounds["maxx"][0]
y0=area.bounds["miny"][0]
y1=area.bounds["maxy"][0]
points=[]
for i in range(int(ceil(x0)),int(ceil(x1)),width):
    for j in range(int(ceil(y0)),int(ceil(y1)),width):
        points.append((i+offset,j+offset))

pointsgeom=[]
pointsgeomshifted=[]
for point in points:
    if Point(point).within(boundary_poly):
        pointsgeomshifted.append( Point( point ) )
        point=(point[0]-offset,point[1]-offset)
        pointsgeom.append(Point(point))

#Plots

# Centre-shifted point plot
area.plot(ax=ax[0][1])
p=GeoSeries(pointsgeomshifted)
p.plot(ax=ax[0][1],color="red",markersize=8)

# Raw points and cell boundary plot
area.plot(ax=ax[1][0])
q=GeoSeries(pointsgeom)
q.plot(ax=ax[1][0],color="red",markersize=8)
for point in pointsgeom:
    rect=patches.Rectangle((point.x,point.y),width,width,linewidth=1,edgecolor='r',facecolor='none')
    ax[1][0].add_patch(rect)


plt.show()