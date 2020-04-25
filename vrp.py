from __future__ import print_function

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from geopandas import GeoSeries
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from scipy.spatial import distance_matrix
from shapely.geometry import LinearRing

from main1 import clusters, pointsgeom, area, width


def create_distance_matrix(req_points) :  # calculating distance matrix
    dist_matrix = distance_matrix( req_points, req_points )
    return dist_matrix  # returing the distance matrix


def create_data_model(dist_matrix) :
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = dist_matrix  # l is the distance matrix
    data['num_vehicles'] = 1  # assuming we have only one vechile
    data['depot'] = 0  # this is depot point
    return data


def print_solution(data, manager, routing, solution) :
    """Prints solution on console."""
    max_route_distance = 0
    solution_list = []  # stores solutions as a list of lists
    for vehicle_id in range( data['num_vehicles'] ) :
        index = routing.Start( vehicle_id )
        plan_output = 'Route for vehicle {}:\n'.format( vehicle_id )
        route_distance = 0
        current_solution = []  # solution of individual vehicles (in this case we only have one)
        while not routing.IsEnd( index ) :
            current_solution.append( manager.IndexToNode( index ) )
            plan_output += ' {} -> '.format( manager.IndexToNode( index ) )
            previous_index = index
            index = solution.Value( routing.NextVar( index ) )
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id )
        solution_list.append( current_solution )
        plan_output += '{}\n'.format( manager.IndexToNode( index ) )
        plan_output += 'Distance of the route: {}m\n'.format( route_distance )
        print( plan_output )
        max_route_distance = max( route_distance, max_route_distance )
    print( 'Maximum of the route distances: {}m'.format( max_route_distance ) )
    return solution_list


def main(dist_matrix) :
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model( dist_matrix )

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager( len( data['distance_matrix'] ),
                                            data['num_vehicles'], data['depot'] )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel( manager )

    # Create and register a transit callback.
    def distance_callback(from_index, to_index) :
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode( from_index )
        to_node = manager.IndexToNode( to_index )
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback( distance_callback )

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles( transit_callback_index )

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        20000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name )
    distance_dimension = routing.GetDimensionOrDie( dimension_name )
    distance_dimension.SetGlobalSpanCostCoefficient( 100 )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters( search_parameters )

    # Print solution on console.
    if solution :
        return print_solution( data, manager, routing, solution )


if __name__ == '__main__' :
    fig, ax = plt.subplots( 1 )
    colors = ['black', 'green', 'yellow', 'orange', 'brown']
    for cluster in clusters :
        dist_matrix = create_distance_matrix( cluster )
        solution_index = main( dist_matrix )  # Solution when we have multiple clusters

        solution_list = []
        for solution in solution_index :
            solution_list.append( cluster[index] for index in solution )
        geo_solution = []  # List to store individual solutions as GeoSeries
        for path in solution_list :
            geo_path = GeoSeries( LinearRing( path ) )
            geo_solution.append( geo_path )

        ax.set_title( 'Cell boundary plot' )
        area.plot( ax=ax, facecolor='none', edgecolor='blue' )
        q = GeoSeries( pointsgeom )
        q.plot( ax=ax, color="red", markersize=1 )

        # Plotting Cell Boundaries
        for point in pointsgeom :
            rect = patches.Rectangle( (point.x, point.y), width, width, linewidth=1, edgecolor='r', facecolor='none' )
            ax.add_patch( rect )

        # Plotting the trips in each cluster
        for i, trip in enumerate( geo_solution ) :
            current_color = colors.pop( i )
            trip.plot( ax=ax, color=current_color, markersize=1 )
            colors.append( current_color )

    plt.show()
