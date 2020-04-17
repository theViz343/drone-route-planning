# This file converts a LineString shapefile to a single polygon shape
# using the convex hull
# functions of the Shapely library.
# A map of districts of Maharashtra is used for this example.
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
import geopandas
import matplotlib.patches as patches
from geopandas import GeoSeries
from shapely.geometry import Polygon,Point,MultiLineString


def squareInside(point, width, poly):
    x=point.x
    y=point.y
    # - -
    # 0 -
    if point.within(poly):
        return True

    # - -
    # - 0
    point=Point(x+width, y)
    if point.within(poly):
        return True

    # - 0
    # - -
    point=Point(x+width, y+width)
    if point.within(poly):
        return True

    # 0 -
    # - -
    point = Point(x, y+width)
    if point.within(poly):
        return True

    return False # No corner is inside polygon

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
width=0.4
offset=width/2
x0=area.bounds["minx"][0]-width
x1=area.bounds["maxx"][0]+width
y0=area.bounds["miny"][0]-width
y1=area.bounds["maxy"][0]+width
boundaryPointsx=[x0,x0,x1,x1,x0]
boundaryPointsy=[y0,y1,y1,y0,y0]
ax[0][0].plot(boundaryPointsx, boundaryPointsy, color='g')
ax[0][1].plot(boundaryPointsx, boundaryPointsy, color='g')
ax[1][0].plot(boundaryPointsx, boundaryPointsy, color='g')
points=[]
for i in np.arange(x0,x1,width):
    for j in np.arange(y0,y1,width):
        points.append((i,j))

pointsgeom=[]
pointsgeomshifted=[]
for point in points:
    if squareInside(Point(point),width,boundary_poly):
        pointsgeom.append( Point( point ) )
        point=(point[0]+offset,point[1]+offset)
        pointsgeomshifted.append(Point(point))

#Plots

# Centre-shifted point plot
area.plot(ax=ax[0][1])
p=GeoSeries(pointsgeomshifted)
p.plot(ax=ax[0][1],color="red",markersize=1)

# Raw points and cell boundary plot
area.plot(ax=ax[1][0])
q=GeoSeries(pointsgeom)
q.plot(ax=ax[1][0],color="red",markersize=1)
for point in pointsgeom:
    rect=patches.Rectangle((point.x,point.y),width,width,linewidth=0.5,edgecolor='r',facecolor='none')
    ax[1][0].add_patch(rect)


plt.show()