# player.py


class Player:
    def __init__(self, name, color, transparent_color, start_x, start_y):
        self.name = name
        self.color = color  # color of base
        self.claim_color = (0, 0, 255)
        self.transparent_color = transparent_color
        self.score = 100
        self.owned_tiles = set()
        self.start_tile = (start_x, start_y)
        self.owned_tiles.add(self.start_tile)

    def owns(self, x, y):
        return (x, y) in self.owned_tiles

    def is_adjacent_to_owned(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in self.owned_tiles:
                    return True
        return False

    def calculate_score_or_income(self, tile_map):
        total = 0
        for row in tile_map:
            for tile in row:
                if tile.owner == self:
                    if tile.is_center or tile.tile_type == "gold":
                        total += 100
                    elif tile.tile_type == "stone":
                        total += 20
        return total

    def calculate_points(self, tile_map):
        self.score += (self.calculate_income(tile_map)/2)  # income plus old points

    def calculate_income(self, tile_map):
        return self.calculate_score_or_income(tile_map)

    def claim_tile(self, x, y, tile_map):
        # Eğer başka oyuncu sahipse, sahiplikten çıkar
        current_owner = tile_map[y][x].owner
        if current_owner and current_owner != self:
            current_owner.owned_tiles.discard((x, y))

        self.owned_tiles.add((x, y))
        tile_map[y][x].owner = self

    def remove_disconnected_tiles(self, tile_map):
        from collections import deque

        visited = set()
        queue = deque([self.start_tile])

        connected = set()

        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) in self.owned_tiles:
                connected.add((x, y))
                # 8 yönlü komşular (çaprazlar dahil)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(tile_map[0]) and 0 <= ny < len(tile_map):
                            queue.append((nx, ny))

        # Bağlantısı olmayanları çıkar
        disconnected = self.owned_tiles - connected
        for x, y in disconnected:
            tile_map[y][x].owner = None
        self.owned_tiles = connected




