# func.py


import json
from tile import Tile


def load_map_from_json(filename="map.json"):
    with open(filename, "r") as f:
        tile_type_map = json.load(f)
    # Convert the Class Tile
    tile_map = [
        [Tile(tile_type) for tile_type in row]
        for row in tile_type_map
    ]
    print(f"The map loaded from '{filename}'.")
    return tile_map

