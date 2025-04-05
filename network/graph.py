class NeighbourGraphBuilder:
    """ Class to build a graph of neighbouring connections between stations."""

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """

        # Initialise the graph as an empty dictionary
        graph = {}

        # Try block to test for invalid input to build function
        try:
            # Iterate through all the connections in tube map
            for connection in tubemap.connections:
                # Extract the station instances of the two connected stations
                stationA, stationB = connection.stations
                # Add station pairs to graph
                self.add_to_station_neighbours(graph, stationA, stationB, connection)
                # Repeat for bidirectional case by swapping input stations to function
                self.add_to_station_neighbours(graph, stationB, stationA, connection)
        except AttributeError:
            print('Input to build function is invalid, returning empty dict for graph variable.')
            graph = {}

        return graph

    def add_to_station_neighbours(self, graph, station1, station2, connection):
        """
            Adds a connection between two stations (station1 and station2) to a graph
            of station neighbours. The connection is added to the list of connections
            associated with the edge between the two stations.

            Args:
                graph (dict): The graph where the key is a station ID (station1) and the
                              value is a dictionary that maps neighbouring station IDs
                              (station2) to a list of Connection instances.
                station1 (Station): The first station in the connection.
                station2 (Station): The second station in the connection.
                connection (Connection): The connection instance representing the link
                                         between the two stations.

            Returns:
                None
            """
        # Add the connection to station 1 to the list of station 1's neighbours.
        if station1.id not in graph:
            graph[station1.id] = {}                # Initialise empty dictionary for the inner dictionary
        if station2.id not in graph[station1.id]:  # If stationB not in neighbours of stationA already then create new empty list for connection instances
            graph[station1.id][station2.id] = []
        graph[station1.id][station2.id].append(connection) # Append the connection instance to the list

        # If it is the second appearance of station pair,
        # connection is appended to existing list without creating new nested list or dictionary.

        return

def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("./data/london.json")
    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)
    print(graph)

if __name__ == "__main__":
    test_graph()
