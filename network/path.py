from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Class to find the shortest path between two stations in a TubeMap.
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap
        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)

    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        # Check if graph is empty from invalid input to .build() method
        if self.graph == {}:
            return None

        # Invert tubemap.stations dictionary to then convert station name strings to id
        conversion_dict = {value.name: key for key, value in self.tubemap.stations.items()}

        # Check if start or end station names are invalid
        if start_station_name not in conversion_dict or end_station_name not in conversion_dict:
            print('Input stations not valid. Please enter valid station names.')
            return None

        # Get station IDs from names

        start_station_id = conversion_dict[start_station_name]
        end_station_id = conversion_dict[end_station_name]

        # If start and end stations are the same, return the start station instance
        if start_station_id == end_station_id:
            return [self.tubemap.stations[start_station_id]]

        # Dijkstra's Algorithm
        return self.run_dijkstra(start_station_id, end_station_id)

    def run_dijkstra(self, start_station_id, end_station_id):
        """
                Runs Dijkstra's algorithm to compute the shortest path between two stations by ID.

                Args:
                    start_station_id (int): The ID of the starting station.
                    end_station_id (int): The ID of the ending station.

                Returns:
                    list[Station]: A list of Station objects representing the shortest path.
                                   If no path is found, returns None.
        """

        dist, prev, queue = self.initialise_data_structures(start_station_id)

        # While queue is not empty
        while len(queue) != 0:

            # Get node with min distance in queue
            station_id = min(queue, key=lambda k: dist[k])

            # Check if goal is reached
            if station_id == end_station_id:
                break

            # Remove station_id from queue
            queue.remove(station_id)

            # Explore neighbours and find min distance.
            neighbours = self.graph[station_id]

            # Find valid neighbours
            valid_neighbours = {neighbour: value for neighbour, value in neighbours.items() if neighbour in queue}

            # Update neighbour distance if necessary
            dist, prev = self.update_neighbour_distances(valid_neighbours, dist, station_id, prev)

        # Reconstruct the shortest path
        return self.reconstruct_path(end_station_id, prev)

    def update_neighbour_distances(self, valid_neighbours, dist, station_id, prev):
        """
                Updates the distances for the valid neighboring stations during Dijkstra's algorithm.

                Args:
                    valid_neighbours (dict): A dictionary of neighboring stations and their connection times.
                    dist (dict): A dictionary of the current shortest distances to each station.
                    station_id (int): The ID of the current station being processed.
                    prev (dict): A dictionary of the previous station for each station in the shortest path.

                Returns:
                    tuple: Updated `dist` and `prev` dictionaries.
        """
        for neighbour in valid_neighbours:
            # Extract the shortest connection to the given neighbour
            connections = valid_neighbours[neighbour]   # List of connection instances
            min_connection = min(connections, key=lambda connection: connection.time)   # Extract connection with min time

            # Total distance = current node’s distance + distance to neighbor
            alt = dist[station_id] + min_connection.time
            # If the distance is shorter than what is stored already for the neighbour, update with new distance
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour] = station_id

        return dist, prev

    def initialise_data_structures(self, start_station_id):
        """
                Initializes the distance, previous, and queue data structures used in Dijkstra's algorithm.

                Args:
                    start_station_id (int): The ID of the starting station.

                Returns:
                    tuple: A tuple containing the `dist`, `prev`, and `queue` data structures:
                        - `dist` (dict): A dictionary with station IDs as keys and distances as values.
                        - `prev` (dict): A dictionary with station IDs as keys and their previous station ID in the shortest path.
                        - `queue` (list): A list of station IDs representing the unprocessed stations.
        """
        dist = {}
        prev = {}
        queue = []

        for station_id in self.graph:
            dist[station_id] = float('inf')
            prev[station_id] = None
            queue.append(station_id)
        dist[start_station_id] = 0

        return dist, prev, queue

    def reconstruct_path(self, end_station_id, prev):
        """
                Reconstructs the shortest path by backtracking through the previous stations.

                Args:
                    end_station_id (int): The ID of the ending station.
                    prev (dict): A dictionary of the previous station for each station in the shortest path.

                Returns:
                    list[Station]: A list of Station objects representing the shortest path.
        """
        id_path = []
        station_id = end_station_id
        while station_id:                   # Loops until it station_id is none
            id_path.append(station_id)
            station_id = prev[station_id]   # Update new station id using prev dictionary
        path = [self.tubemap.stations[station_id] for station_id in id_path]
        path = path[::-1]
        return path

def test_shortest_path():
    """
        A simple test case to validate the correctness of the shortest path algorithm.

        Tests the shortest path from "Covent Garden" to "Green Park" and checks if the output matches the expected path.
    """
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("./data/london.json")
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()

