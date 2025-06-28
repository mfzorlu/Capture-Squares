# tile.py


class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type
        self.owner = None  # such as Player
        self.is_center = False

        if tile_type == "gold":
            self.color = (255, 215, 0)
            self.movement_point = 100
        elif tile_type == "stone":
            self.color = (128, 128, 128)
            self.movement_point = 20
        else:
            self.color = (0, 0, 0)
            self.movement_point = 0


