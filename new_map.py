import json
import random
from time import sleep

MAP_WIDTH = 1000
MAP_HEIGHT = 1000

def generate_map():
    tile_map = []
    for _ in range(MAP_HEIGHT):
        row = []
        for _ in range(MAP_WIDTH):
            # Possibility of Gold 1/15
            tile_type = "gold" if random.randint(1, 15) == 1 else "stone"
            row.append(tile_type)
        tile_map.append(row)
    return tile_map

def save_map_to_json(tile_map, filename="map.json"):
    with open(filename, "w") as f:
        json.dump(tile_map, f)
    print(f"The map recorded in '{filename}'.")

# generate a map and load it
my_map = generate_map()
save_map_to_json(my_map)

print("new map has generated.")
sleep(3)
