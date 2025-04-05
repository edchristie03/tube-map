import json
from json import JSONDecodeError
from tube.components import Station, Line, Connection

class TubeMap:
    """
    The TubeMap class models a London Underground system, which includes stations,
    lines, and connections between stations.

    This class allows for importing data from a JSON file to populate the
    stations, lines, and connections attributes.

    Attributes:
        stations (dict): A dictionary mapping station ID (str) to Station instances.
        lines (dict): A dictionary mapping line ID (str) to Line instances.
        connections (list): A list of Connection instances representing the connections
                            between stations on various lines.
    """

    def __init__(self):
        """Initializes an empty TubeMap with no stations, lines, or connections."""
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        """Imports tube map information from a JSON file.

        This method reads a JSON file at the specified `filepath` and updates
        the `stations`, `lines`, and `connections` attributes accordingly.

        Note:
            If the indicated zone is not an integer (for example: "2.5"), it
            means the station belongs to two zones. For instance, "2.5" indicates
            that the station belongs to both zone 2 and zone 3.

        If the `filepath` is invalid or the file cannot be parsed, the method
        returns without modifying the attributes.

        Args:
            filepath (str): The relative or absolute path to the JSON file containing
                            the tube map data.

        Returns:
            None
        """
        try:
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, JSONDecodeError, TypeError, OSError):
            print('Invalid input to import_from_json function')
            return 1

        self.initiate_stations(data)
        self.initiate_lines(data)
        self.initiate_connections(data)

        return

    def initiate_stations(self, data):      # Initiate self.stations
        """Helper method to initialize the `stations` attribute from JSON data.

        Parses the station information from the JSON file and creates Station
        instances for each station. If the station belongs to multiple zones,
        it appropriately handles the zone information.
        Args:
            data (dict): The parsed JSON data containing stations information.

        Returns:
                None
        """
        stations_data = data['stations']

        for station in stations_data:
            station_id = station['id']          # Get id str
            name = station['name']              # Get name str
            zone = float(station['zone'])

            # If station in two zones, create set of the integers
            if zone % 1 != 0:
                zone = {int(zone - 0.5), int(zone + 0.5)}
            else:
                zone = {int(zone)}
            # Create Station instance
            self.stations[station_id] = Station(station_id, name, zone)

        return

    def initiate_lines(self, data):         # Initiate self.lines
        """Helper method to initialize the `lines` attribute from JSON data.

        Parses the line information from the JSON file and creates Line instances for each line.

        Args:
            data (dict): The parsed JSON data containing lines information.

        Returns:
            None
        """
        lines_data = data['lines']
        for line in lines_data:
            line_id = line['line']  # str
            name = line['name']     # str
            self.lines[line_id] = Line(line_id, name)

        return

    def initiate_connections(self, data):   # Initiate self.connections
        """Helper method to initialize the `connections` attribute from JSON data.

        Parses the connection information from the JSON file and creates Connection
        instances for each connection between stations. Each connection involves
        two stations, a line, and the travel time between the stations.

        Args:
            data (dict): The parsed JSON data containing connections information.

        Returns:
            None
        """
        connections_data = data['connections']
        for connection in connections_data:
            station1 = connection['station1']       # Get station id
            station2 = connection['station2']       # Get station id
            line_id = connection['line']
            time = int(connection['time'])
            stations = {self.stations[station1], self.stations[station2]}   # Index self.stations dict to get station instance
            line = self.lines[line_id]                                      # Index self.lines dict to get line instance
            self.connections.append(Connection(stations, line, time))

        return

def test_import():
    tubemap = TubeMap()

    # Only run test if input file is correct. If there is error, import_from_json will return 1

    if tubemap.import_from_json("./data/london.json") != 1:
    
        # view one example Station
        print(tubemap.stations[list(tubemap.stations)[0]])

        # view one example Line
        print(tubemap.lines[list(tubemap.lines)[0]])

        # view the first Connection
        print(tubemap.connections[0])

        # view stations for the first Connection
        print([station for station in tubemap.connections[0].stations])

if __name__ == "__main__":
    test_import()
