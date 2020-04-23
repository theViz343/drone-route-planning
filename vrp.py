from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from main1 import clusters,noOfClusters,total_points,centroids
from shapely.geometry import Point, MultiLineString, MultiPoint, Polygon
from sklearn.cluster import KMeans
import math
def create_distance_matrix():                       #calculating distance matrix
    l=[[]]*(total_points)                           #total length of matrix is same as totla points
    j=0
    # print(a)
    for i in range(noOfClusters):                       #looping over points to calculate the distance matrix
        for point1 in  MultiPoint(clusters[i]):                    
                for point2 in MultiPoint(clusters[i]):
                    distance=math.sqrt(((point1.x-point2.x)**2)+((point1.y-point2.y)**2))   # i have hard coded the matrix
                    l[j].append(distance)                                                   
                j=j+1
    # print(l)
    return l                                            #returing the distance matrix


def create_data_model(l):                   
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = l                 #l is the distance matrix
    # print("hhh")
    # print(l)
    data['num_vehicles'] = 1                    #assuming we have only one vechile
    data['depot'] =0                            #this is depot point
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))




def main(l):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(l)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    l=create_distance_matrix()  
    main(l)                             #this  gives solution if do not make clusters
    j=0
    j=clusters[0].shape[0]              #   this made to access the distance matrix for each clusters 
    for i in range(noOfClusters):       #this calculate path for each cluster
        if i==0:    
            a=l[ :j]                   #  for 1st clusters total point in distance matrix is first j element
            main(a)
        elif i==noOfClusters-1:
            a=l[j:]                 #for last clusters
            main(a)
        else:
            a=l[j:j+clusters[i].shape[0]]
            j+=clusters[i].shape[0]
            main(a)                         #for rest of clusters
