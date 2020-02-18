import matplotlib.pyplot as plt
from geopandas import GeoSeries
from shapely.geometry import Polygon,Point
poly = Polygon([(0, 0), (10, 0), (20, 20),(10, 40),(-20, 30),(-10, 10)])
g = GeoSeries(poly)
width=5
offset=width/2
x0=g.bounds["minx"][0]
x1=g.bounds["maxx"][0]
y0=g.bounds["miny"][0]
y1=g.bounds["maxy"][0]
points=[]
for i in range(int(x0),int(x1),width):
    for j in range(int(y0),int(y1),width):
        points.append((i+offset,j+offset))

pointsgeom=[]
for point in points:
    if Point(point).within(poly):
        pointsgeom.append(Point(point))

p=GeoSeries(pointsgeom)
print(p)
g.plot()
p.plot()
plt.show()