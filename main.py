import pygame
import random
import time
import func
from colors import colors
from player import Player
from menu import show_menu, get_player_names

# --- Ekran Boyutları ---
PANEL_WIDTH = 240
GAME_WIDTH = 640
SCREEN_WIDTH = GAME_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = 640

# --- Pygame Başlat ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Capture Squares")
font = pygame.font.Font("fonts/Orbitron-Regular.ttf", 16)
clock = pygame.time.Clock()

# --- Menü ve Oyuncu Adlarını Al ---
if show_menu(screen) == "2P":
    player1_name, player2_name = get_player_names(screen)
else:
    pygame.quit()
    exit()

# --- Harita ve Oyuncular ---
tile_map = func.load_map_from_json()
available_colors = random.sample(colors, 2)

player1 = Player(player1_name, available_colors[0]["color"], available_colors[0]["transparent"], 500, 500)
player2 = Player(player2_name, available_colors[1]["color"], available_colors[1]["transparent"], 505, 500)

tile_map[500][500].is_center = True
tile_map[500][500].owner = player1
tile_map[500][505].is_center = True
tile_map[500][505].owner = player2

players = [player1, player2]
turn_index = 0
current_player = players[turn_index]
selected_player_index = 0  # sırası gelen oyuncunun bilgileri açık başlar

# --- Kamera ve Tile Ayarları ---
tile_size = 32
camera_x = 490
camera_y = 490
MOVEMENT_COST = 100
MAP_WIDTH = len(tile_map[0])
MAP_HEIGHT = len(tile_map)

# --- Yardımcı Fonksiyon ---
def center_camera_on_player(player, viewport_width, viewport_height):
    global camera_x, camera_y
    center_x, center_y = player.start_tile
    camera_x = max(0, min(center_x - viewport_width // 2, MAP_WIDTH - viewport_width))
    camera_y = max(0, min(center_y - viewport_height // 2, MAP_HEIGHT - viewport_height))

# --- Oyun Döngüsü ---
show_turn_box = True
turn_box_start_time = time.time()
running = True

while running:
    viewport_width = GAME_WIDTH // tile_size
    viewport_height = SCREEN_HEIGHT // tile_size
    panel_x = GAME_WIDTH

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x = camera_x + mouse_x // tile_size
            tile_y = camera_y + mouse_y // tile_size

            if mouse_x < GAME_WIDTH and 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
                tile = tile_map[tile_y][tile_x]
                if tile.owner is None and current_player.is_adjacent_to_owned(tile_x, tile_y):
                    if current_player.score >= MOVEMENT_COST:
                        current_player.claim_tile(tile_x, tile_y, tile_map)
                        tile.owner = current_player
                        current_player.score -= MOVEMENT_COST
            elif panel_x <= mouse_x <= SCREEN_WIDTH:
                item_height = 40
                for idx, player in enumerate(players):
                    y_top = 20 + idx * item_height
                    if y_top <= mouse_y <= y_top + item_height:
                        selected_player_index = idx
                        break

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_PLUS, pygame.K_EQUALS, pygame.K_w]:
                tile_size = min(tile_size + 4, 64)
            if event.key in [pygame.K_MINUS, pygame.K_s]:
                tile_size = max(tile_size - 4, 8)
            if event.key == pygame.K_SPACE:
                turn_index = (turn_index + 1) % len(players)
                current_player = players[turn_index]
                current_player.calculate_points(tile_map)
                current_player.remove_disconnected_tiles(tile_map)
                current_player.calculate_points(tile_map)
                center_camera_on_player(current_player, viewport_width, viewport_height)
                show_turn_box = True
                turn_box_start_time = time.time()
                selected_player_index = turn_index

    # --- Kamera Tuşları ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x = max(camera_x - 1, 0)
    if keys[pygame.K_RIGHT]:
        camera_x = min(camera_x + 1, MAP_WIDTH - viewport_width)
    if keys[pygame.K_UP]:
        camera_y = max(camera_y - 1, 0)
    if keys[pygame.K_DOWN]:
        camera_y = min(camera_y + 1, MAP_HEIGHT - viewport_height)

    # --- Ekranı Temizle ---
    screen.fill((0, 0, 0))

    # --- Haritayı Çiz ---
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

    # --- Koordinat Bilgisi ---
    cam_text = font.render(f"Camera: ({camera_x}, {camera_y})", True, (200, 200, 200))
    screen.blit(cam_text, (10, SCREEN_HEIGHT - 30))

    # --- Sağ Panel ---
    panel_x = SCREEN_WIDTH - PANEL_WIDTH
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_WIDTH, SCREEN_HEIGHT))  # panel background

    item_height = 80
    card_padding = 10
    card_margin = 20

    for idx, player in enumerate(players):
        y_pos = card_margin + idx * (item_height + card_margin)

        # Kutunun rengi (seçiliyse açık gri)
        bg_color = (70, 70, 70) if idx == selected_player_index else (50, 50, 50)
        pygame.draw.rect(screen, bg_color, (panel_x + card_padding, y_pos, PANEL_WIDTH - 2 * card_padding, item_height),
                         border_radius=8)

        # İsim ve merkez koordinatları
        name_text = font.render(f"{player.name} ({player.start_tile[0]}, {player.start_tile[1]})", True,
                                (255, 255, 255))
        screen.blit(name_text, (panel_x + 20, y_pos + 10))

        # Sadece seçili oyuncunun detayları
        if idx == selected_player_index:
            income = player.calculate_income(tile_map)
            detail_text1 = font.render(f"Points: {int(player.score)}", True, (200, 200, 200))
            detail_text2 = font.render(f"Income: {int(income)}", True, (200, 200, 200))
            screen.blit(detail_text1, (panel_x + 20, y_pos + 30))
            screen.blit(detail_text2, (panel_x + 20, y_pos + 50))

    # --- Sıra Gösterim Kutusu ---
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
