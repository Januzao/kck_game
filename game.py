# import pygame
# import sys
#
# def main():
#     pygame.init()
#
#     # 1) Завантажуємо основне зображення
#     image = pygame.image.load("photo.png")
#     width, height = image.get_width(), image.get_height()
#
#     # 2) Встановлюємо масштаб і створюємо вікно
#     scale = 16
#     screen = pygame.display.set_mode((width * scale, height * scale))
#     pygame.display.set_caption("Заміна сірого пікселя картинкою")
#
#     # 3) Завантажуємо замінну картинку з альфою і масштабуємо
#     replace_img = pygame.image.load("c1c1c1f.png").convert_alpha()
#     replace_img = pygame.transform.scale(replace_img, (scale, scale))
#
#     # 4) Визначаємо точний відтінок сірого
#     TARGET_GRAY = (193, 193, 193)
#
#     clock = pygame.time.Clock()
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         # 5) Рендеримо кожен піксель
#         for y in range(height):
#             for x in range(width):
#                 color = image.get_at((x, y))
#                 rgb = (color.r, color.g, color.b)
#
#                 if rgb == TARGET_GRAY:
#                     # тільки для #C1C1C1 — малюємо вашу картинку
#                     screen.blit(replace_img, (x * scale, y * scale))
#                 else:
#                     # для всіх інших — заливка початковим кольором
#                     rect = pygame.Rect(x * scale, y * scale, scale, scale)
#                     screen.fill(color, rect)
#
#         pygame.display.flip()
#         clock.tick(60)
#
#     pygame.quit()
#     sys.exit()
#
# if __name__ == "__main__":
#     main()
import os
import sys
import pygame

def create_sprite_map_surface(map_path, sprite_dir):
    """
    Зчитує test_map.png і для кожного пікселя з кольором (R,G,B)
    підставляє спрайт із папки sprites/ (файли R_G_B.png),
    без попереднього встановлення відеорежиму.
    Повертає surface карти та ширину, висоту одного тайла.
    """
    # 1) Просто завантажуємо зображення
    map_img = pygame.image.load(map_path)
    map_w, map_h = map_img.get_width(), map_img.get_height()

    # 2) Підвантажуємо спрайти й зберігаємо їх в словник
    sprite_mapping = {}
    tile_w = tile_h = None
    for fn in os.listdir(sprite_dir):
        if not fn.lower().endswith(".png"):
            continue
        base, _ = os.path.splitext(fn)
        parts = base.split("_")
        if len(parts) != 3:
            continue
        try:
            r, g, b = map(int, parts)
        except ValueError:
            continue

        spr = pygame.image.load(os.path.join(sprite_dir, fn)).convert_alpha()
        if tile_w is None:
            tile_w, tile_h = spr.get_size()
        sprite_mapping[(r, g, b)] = spr

    if tile_w is None:
        raise RuntimeError("У папці sprites/ не знайдено жодного .png")

    # 3) Малюємо тайл-мапу у власному розмірі (map_w*tile_w × map_h*tile_h)
    canvas = pygame.Surface((map_w*tile_w, map_h*tile_h), pygame.SRCALPHA)
    for y in range(map_h):
        for x in range(map_w):
            c = map_img.get_at((x, y))
            key = (c.r, c.g, c.b)
            if key in sprite_mapping:
                canvas.blit(sprite_mapping[key], (x*tile_w, y*tile_h))
            else:
                canvas.fill(key, pygame.Rect(x*tile_w, y*tile_h, tile_w, tile_h))

    return canvas, tile_w, tile_h

def main():
    pygame.init()

    # 1) Створимо resizable-вікно з якимось початковим розміром
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tile Map Viewer (Resizable)")

    # 2) Завантажуємо карту в сирому вигляді
    map_surf, tile_w, tile_h = create_sprite_map_surface("test_map.png", "sprites")
    map_w, map_h = map_surf.get_width(), map_surf.get_height()

    clock = pygame.time.Clock()
    scaled_map = None
    last_size = (0, 0)
    offset = (0, 0)

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.VIDEORESIZE:
                # при зміні розміру вікна — оновлюємо screen
                screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)

        win_w, win_h = screen.get_size()
        # Якщо розмір вікна змінився — пересчитаємо масштабовану карту
        if (win_w, win_h) != last_size:
            # знаходимо коефіцієнт, щоб вся карта вмістилась
            scale = min(win_w / map_w, win_h / map_h)
            new_w = int(map_w * scale)
            new_h = int(map_h * scale)
            # масштабюємо
            scaled_map = pygame.transform.smoothscale(map_surf, (new_w, new_h))
            # центр поєднуємо
            offset = ((win_w - new_w) // 2, (win_h - new_h) // 2)
            last_size = (win_w, win_h)

        # 3) Малюємо
        screen.fill((0, 0, 0))
        if scaled_map:
            screen.blit(scaled_map, offset)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Переконайтесь, що поруч:
    # - test_map.png
    # - папка sprites/ з файлами "R_G_B.png"
    main()
