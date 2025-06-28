# Capture Squares Game File

import pygame
import random
import time
import func
from colors import colors
from player import Player

# Load the Map
tile_map = func.load_map_from_json()

# Rastgele oyuncu renkleri seç
available_colors = random.sample(colors, 2)
player1 = Player("Player 1", available_colors[0]["color"], available_colors[0]["transparent"], 500, 500)
player2 = Player("Player 2", available_colors[1]["color"], available_colors[1]["transparent"], 505, 500)
tile_map[500][500].is_center = True
tile_map[500][505].is_center = True
tile_map[500][500].owner = player1
tile_map[500][505].owner = player2

players = [player1, player2]
turn_index = 0
current_player = players[turn_index]
selected_player_index = 0

MOVEMENT_COST = 100
MAP_WIDTH = len(tile_map[0])
MAP_HEIGHT = len(tile_map)

# Görüntü ayarları
PANEL_WIDTH = 240
GAME_WIDTH = 640
SCREEN_WIDTH = GAME_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = 640
tile_size = 32
viewport_width = GAME_WIDTH // tile_size
viewport_height = SCREEN_HEIGHT // tile_size

camera_x, camera_y = 490, 490

# Pygame başlat
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alan Kapmaca - Capture Squares")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

show_turn_box = True
turn_box_start_time = time.time()

# Fonksiyonlar
def center_camera_on_player(player, viewport_width, viewport_height):
    global camera_x, camera_y
    center_x, center_y = player.start_tile
    camera_x = max(0, min(center_x - viewport_width // 2, MAP_WIDTH - viewport_width))
    camera_y = max(0, min(center_y - viewport_height // 2, MAP_HEIGHT - viewport_height))

def draw_text_with_shadow(surface, text, font, pos, color, shadow_color=(0, 0, 0)):
    shadow_pos = (pos[0] + 1, pos[1] + 1)
    shadow_surf = font.render(text, True, shadow_color)
    text_surf = font.render(text, True, color)
    surface.blit(shadow_surf, shadow_pos)
    surface.blit(text_surf, pos)

center_camera_on_player(current_player, viewport_width, viewport_height)

# Ana döngü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_x < GAME_WIDTH:  # oyun alanı tıklaması
                tile_x = camera_x + mouse_x // tile_size
                tile_y = camera_y + mouse_y // tile_size
                if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                    tile = tile_map[tile_y][tile_x]
                    if tile.owner is None and current_player.is_adjacent_to_owned(tile_x, tile_y):
                        if current_player.score >= MOVEMENT_COST:
                            current_player.claim_tile(tile_x, tile_y)
                            tile.owner = current_player
                            current_player.score -= MOVEMENT_COST
                            print(f"{current_player.name} claimed ({tile_x}, {tile_y}). Remaining: {current_player.score}")
                else:
                    print("Clicked outside map boundaries!")

            else:  # panel tıklaması
                panel_click_y = mouse_y
                item_height = 60
                for index, player in enumerate(players):
                    y_top = 20 + index * item_height
                    if y_top <= panel_click_y <= y_top + item_height:
                        selected_player_index = index if selected_player_index != index else None
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_w):
                tile_size = min(tile_size + 4, 64)
                viewport_width = GAME_WIDTH // tile_size
                viewport_height = SCREEN_HEIGHT // tile_size
            elif event.key in (pygame.K_MINUS, pygame.K_s):
                tile_size = max(tile_size - 4, 8)
                viewport_width = GAME_WIDTH // tile_size
                viewport_height = SCREEN_HEIGHT // tile_size
            elif event.key == pygame.K_SPACE:
                turn_index = (turn_index + 1) % len(players)
                current_player = players[turn_index]
                current_player.calculate_points(tile_map)
                center_camera_on_player(current_player, viewport_width, viewport_height)

                selected_player_index = turn_index  # next player
                show_turn_box = True
                turn_box_start_time = time.time()

    # Kamera hareketi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: camera_x = max(camera_x - 1, 0)
    if keys[pygame.K_RIGHT]: camera_x = min(camera_x + 1, MAP_WIDTH - viewport_width)
    if keys[pygame.K_UP]: camera_y = max(camera_y - 1, 0)
    if keys[pygame.K_DOWN]: camera_y = min(camera_y + 1, MAP_HEIGHT - viewport_height)

    # Ekranı temizle
    screen.fill((0, 0, 0))

    # Haritayı çiz
    for row in range(viewport_height):
        for col in range(viewport_width):
            map_x = camera_x + col
            map_y = camera_y + row
            tile = tile_map[map_y][map_x]
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)

            pygame.draw.rect(screen, tile.color, rect)
            if tile.owner and not tile.is_center:
                pygame.draw.rect(screen, tile.owner.transparent_color, rect, width=5)
            if tile.is_center:
                pygame.draw.rect(screen, tile.owner.color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, width=1)

    # Kamera koordinatları
    cam_text = font.render(f"Coordinates: ({camera_x}, {camera_y})", True, (200, 200, 200))
    screen.blit(cam_text, (10, SCREEN_HEIGHT - 30))

    # Panel
    panel_x = SCREEN_WIDTH - PANEL_WIDTH
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_WIDTH, SCREEN_HEIGHT))

    item_height = 60
    for idx, player in enumerate(players):
        y_pos = 20 + idx * item_height
        is_selected = (idx == selected_player_index)
        bg_color = (60, 60, 60) if is_selected else (40, 40, 40)
        pygame.draw.rect(screen, bg_color, (panel_x, y_pos, PANEL_WIDTH, item_height))

        draw_text_with_shadow(screen, f"{player.name} ({player.start_tile[0]},{player.start_tile[1]})", font,
                              (panel_x + 10, y_pos), (255, 255, 255))

        if is_selected:
            income = player.calculate_income(tile_map)
            draw_text_with_shadow(screen, f"Points: {player.score}", font, (panel_x + 10, y_pos + 20), (255, 255, 255))
            draw_text_with_shadow(screen, f"Income: {income}", font, (panel_x + 10, y_pos + 40), (255, 255, 255))

    # Geçerli oyuncunun adını ortaya yaz (1 saniyeliğine)
    if show_turn_box and time.time() - turn_box_start_time <= 1:
        box_width, box_height = 300, 50
        box_rect = pygame.Rect((SCREEN_WIDTH - box_width) // 2, (SCREEN_HEIGHT - box_height) // 2, box_width, box_height)
        pygame.draw.rect(screen, (50, 50, 50), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, width=2)
        name_surface = font.render(f"{current_player.name}'s Turn", True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=box_rect.center)
        screen.blit(name_surface, name_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

