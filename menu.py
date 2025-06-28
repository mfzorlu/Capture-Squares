# menu.py


import pygame

def show_menu(screen):
    clock = pygame.time.Clock()
    title_font = pygame.font.Font("fonts/Orbitron-Bold.ttf", 48)

    small_font = pygame.font.Font("fonts/Orbitron-Regular.ttf", 24)

    selected_option = None

    while True:
        screen.fill((30, 30, 30))

        # Title
        title_text = title_font.render("Capture Squares", True, (255, 255, 255))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))

        # Buttons
        btn_2p_rect = pygame.Rect(screen.get_width() // 2 - 100, 250, 200, 50)
        btn_bot_rect = pygame.Rect(screen.get_width() // 2 - 100, 320, 200, 50)

        pygame.draw.rect(screen, (70, 130, 180), btn_2p_rect)
        pygame.draw.rect(screen, (100, 100, 100), btn_bot_rect)  # Inactive

        btn_2p_text = small_font.render("2 Player", True, (255, 255, 255))
        btn_bot_text = small_font.render("Player vs Bot (coming soon)", True, (180, 180, 180))

        screen.blit(btn_2p_text, (btn_2p_rect.centerx - btn_2p_text.get_width() // 2,
                                  btn_2p_rect.centery - btn_2p_text.get_height() // 2))
        screen.blit(btn_bot_text, (btn_bot_rect.centerx - btn_bot_text.get_width() // 2,
                                   btn_bot_rect.centery - btn_bot_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_2p_rect.collidepoint(event.pos):
                    return "2P"

        pygame.display.flip()
        clock.tick(30)


def get_player_names(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font("fonts/Orbitron-Regular.ttf", 18)

    input_boxes = [pygame.Rect(300, 220, 280, 40), pygame.Rect(300, 300, 280, 40)]
    texts = ["", ""]
    active_box = 0
    start_button = pygame.Rect(350, 380, 180, 50)

    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500  # ms

    while True:
        dt = clock.tick(30)  # frame süresi ms cinsinden
        cursor_timer += dt
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        screen.fill((40, 40, 40))

        label1 = font.render("Player 1 Name:", True, (255, 255, 255))
        label2 = font.render("Player 2 Name:", True, (255, 255, 255))
        screen.blit(label1, (input_boxes[0].x, input_boxes[0].y - 25))
        screen.blit(label2, (input_boxes[1].x, input_boxes[1].y - 25))

        for i, box in enumerate(input_boxes):
            color = (200, 200, 200) if i == active_box else (100, 100, 100)
            pygame.draw.rect(screen, color, box, 2)

            display_text = texts[i]
            if i == active_box and cursor_visible:
                display_text += "|"
            text_surface = font.render(display_text, True, (255, 255, 255))
            screen.blit(text_surface, (box.x + 5, box.y + 5))

        pygame.draw.rect(screen, (70, 130, 180), start_button)
        start_text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                 start_button.centery - start_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and all(texts):
                    return texts[0], texts[1]
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    texts[active_box] = texts[active_box][:-1]
                elif event.key == pygame.K_RETURN:
                    active_box = (active_box + 1) % 2
                elif len(texts[active_box]) < 15:
                    if event.unicode.isprintable():
                        texts[active_box] += event.unicode

        pygame.display.flip()
