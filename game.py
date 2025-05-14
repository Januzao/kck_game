import os
import sys
import pygame

TILE_SIZE = 32  # очікуваний розмір кожного тайла (всі спрайти мають бути цього розміру)
SCROLL_SPEED = 10  # швидкість прокрутки

def create_sprite_map_surface(map_path, sprite_dir):
    map_img = pygame.image.load(map_path).convert()
    map_w, map_h = map_img.get_width(), map_img.get_height()

    sprite_mapping = {}
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
        if spr.get_size() != (TILE_SIZE, TILE_SIZE):
            print(f"[WARN] Sprite {fn} is not {TILE_SIZE}x{TILE_SIZE}, resizing...")
            spr = pygame.transform.scale(spr, (TILE_SIZE, TILE_SIZE))

        sprite_mapping[(r, g, b)] = spr

    if not sprite_mapping:
        raise RuntimeError("У папці sprite_dir не знайдено жодного валідного спрайта!")

    # створення поверхні всієї карти
    canvas = pygame.Surface((map_w * TILE_SIZE, map_h * TILE_SIZE), pygame.SRCALPHA)
    for y in range(map_h):
        for x in range(map_w):
            c = map_img.get_at((x, y))
            key = (c.r, c.g, c.b)
            pos = (x * TILE_SIZE, y * TILE_SIZE)
            if key in sprite_mapping:
                canvas.blit(sprite_mapping[key], pos)
            else:
                print(f"[ERROR] Missing sprite for color {key} at tile ({x}, {y})")
                pygame.draw.rect(canvas, (255, 0, 255), (*pos, TILE_SIZE, TILE_SIZE))  # пурпурна заливка

    return canvas

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tile Map Viewer (Camera Scroll)")

    map_surf = create_sprite_map_surface("map_ent.png", "map_ent")
    map_w, map_h = map_surf.get_width(), map_surf.get_height()

    clock = pygame.time.Clock()
    camera_x, camera_y = 0, 0

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x -= SCROLL_SPEED
        if keys[pygame.K_RIGHT]:
            camera_x += SCROLL_SPEED
        if keys[pygame.K_UP]:
            camera_y -= SCROLL_SPEED
        if keys[pygame.K_DOWN]:
            camera_y += SCROLL_SPEED

        # обмежуємо межі карти
        win_w, win_h = screen.get_size()
        camera_x = max(0, min(camera_x, map_w - win_w))
        camera_y = max(0, min(camera_y, map_h - win_h))

        screen.fill((0, 0, 0))
        screen.blit(map_surf, (0, 0), pygame.Rect(camera_x, camera_y, win_w, win_h))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
