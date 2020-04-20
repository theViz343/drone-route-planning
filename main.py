# This file converts a LineString shapefile to a single polygon shape
# using the convex hull
# functions of the Shapely library.
# A map of districts of Maharashtra is used for this example.
import time

import geopandas
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from geopandas import GeoSeries
from shapely.geometry import Point, MultiLineString, MultiPoint, Polygon
from sklearn.cluster import KMeans


def squareInside(point, width, poly) : #new method, more efficient
    x = point.x
    y = point.y
    square = Polygon( [(x, y), (x + width, y), (x + width, y + width), (x, y + width)] )
    return square.intersects( poly )


def cornerInside(point, width, poly) : # very slow, deprecated (don't use)
    x = point.x
    y = point.y
    # - -
    # 0 -
    if point.within( poly ) :
        return True

    # - -
    # - 0
    point = Point( x + width, y )
    if point.within( poly ) :
        return True

    # - 0
    # - -
    point = Point( x + width, y + width )
    if point.within( poly ) :
        return True

    # 0 -
    # - -
    point = Point( x, y + width )
    if point.within( poly ) :
        return True

    return False  # No corner is inside polygon


### Parameters
maha_shape = geopandas.read_file( "maharashtra/maharashtra_administrative.shp" )
width = 0.05
offset = width / 2
noOfClusters = 6
###
start_time = time.time()
# Calculate the Convex Hull of all MultiLineString districts
boundary = []
for district in maha_shape["geometry"] :
    boundary.append( district )

boundary_poly = MultiLineString( boundary ).convex_hull
area = GeoSeries( boundary_poly )

##TimeStamp
check1 = time.time()

# Calculation of points with set width between them

x0 = area.bounds["minx"][0] - width
x1 = area.bounds["maxx"][0] + width
y0 = area.bounds["miny"][0] - width
y1 = area.bounds["maxy"][0] + width
boundaryPointsx = [x0, x0, x1, x1, x0]
boundaryPointsy = [y0, y1, y1, y0, y0]

##TimeStamp
check2 = time.time()

# Calculating point coordinates across the whole boundary
points = []
for i in np.arange( x0, x1, width ) :
    for j in np.arange( y0, y1, width ) :
        points.append( (i, j) )

pointsgeom = []  # normal points python list
pointsgeomshifted = []  # shifted (to the centre of cell boundary) point python list
GridPoints = []  # points numpy array

##TimeStamp
check3 = time.time()

# Calculation of points within the area
for point in points :
    if squareInside( Point( point ), width,
                     boundary_poly ) :  # If you use the old fn now called cornerInside, then its quite slow
        GridPoints.append( point )
        pointsgeom.append( Point( point ) )
        point = (point[0] + offset, point[1] + offset)
        pointsgeomshifted.append( Point( point ) )

total_points = len( pointsgeom )
npGridPoints = np.array( GridPoints )

##TimeStamp
check4 = time.time()

# Clustering of area into different sections
clusteredData = KMeans( n_clusters=noOfClusters ).fit( npGridPoints )
clusters = np.array( [] )
centroids = clusteredData.cluster_centers_
labels = clusteredData.labels_  # labels tell the cluster to which a given point corresponds to
collection = []
for i in range( noOfClusters ) :
    collection.append( npGridPoints[labels == i] )

clusters = np.append( clusters, collection, axis=0 )

##TimeStamp
check5 = time.time()

# Time calculation
total_time = check5 - start_time
print( "Total calculation time is " + str( total_time ) + "s" )
convex_hull_time = check1 - start_time
print( "Convex Hull formation time is " + str( convex_hull_time ) + "s" )
boundary_time = check2 - check1
print( "boundary formation time is " + str( boundary_time ) + "s" )
pointifying_time = check3 - check2
print( "Pointifying time is " + str( pointifying_time ) + "s" )
inside_time = check4 - check3
print( "Inside or not calculation time is " + str( inside_time ) + "s" )
clustering_time = check5 - check4
print( "Clustering time is " + str( clustering_time ) + "s" )
# Plots
fig, ax = plt.subplots( 2, 2 )

# Boundaries of the plots so that they scale equally (might be unnecessary)
ax[0][0].plot( boundaryPointsx, boundaryPointsy, color='g' )
ax[0][1].plot( boundaryPointsx, boundaryPointsy, color='g' )
ax[1][0].plot( boundaryPointsx, boundaryPointsy, color='g' )
ax[1][1].plot( boundaryPointsx, boundaryPointsy, color='g' )

# PLOT1: Plot shapefile info directly
ax[0][0].set_title( 'Shapefile' )
maha_shape.plot( ax=ax[0][0] )

# PLOT2: Centre-shifted point plot
ax[0][1].set_title( 'Centre-shifted points' )
area.plot( ax=ax[0][1], facecolor='none', edgecolor='blue' )
p = GeoSeries( pointsgeomshifted )
p.plot( ax=ax[0][1], color="red", markersize=1 )

# PLOT3: Raw points and cell boundary plot
ax[1][0].set_title( 'Cell boundary plot' )
area.plot( ax=ax[1][0], facecolor='none', edgecolor='blue' )
q = GeoSeries( pointsgeom )
q.plot( ax=ax[1][0], color="red", markersize=1 )
for point in pointsgeom :
    rect = patches.Rectangle( (point.x, point.y), width, width, linewidth=1, edgecolor='r', facecolor='none' )
    ax[1][0].add_patch( rect )

# PLOT4: Colored clustered plot with cell boundaries
ax[1][1].set_title( 'Clustered plot' )
colors = ['red', 'black', 'green', 'yellow', 'orange', 'brown']
area.plot( ax=ax[1][1], facecolor='none', edgecolor='blue' )

geocentroids = GeoSeries( MultiPoint( centroids ) )
geocentroids.plot( ax=ax[1][1], color=colors[-1], markersize=50 )

for i in range( noOfClusters ) :
    geocluster = GeoSeries( MultiPoint( clusters[i] ) )
    geocluster.plot( ax=ax[1][1], color=colors[i], markersize=1 )  # printing cluster points
    for point in MultiPoint( clusters[i] ) :
        rect = patches.Rectangle( (point.x, point.y), width, width, linewidth=1, edgecolor=colors[i],
                                  facecolor='none' )
        ax[1][1].add_patch( rect )  # printing cell boundary
    print( 'Size of cluster', i, "is", clusters[i].shape[0] )

print( total_points )

plt.show()