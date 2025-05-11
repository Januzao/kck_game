import pygame
import os
from PIL import Image  # Щоб зчитувати пікселі з PNG

# Ініціалізація Pygame
pygame.init()

# --- Налаштування ---
TILE_SIZE = 32  # Розмір тайла (можна змінити)
MAP_PATH = "src/maps/map1.png"
WALLS_DIR = "src/walls"
FLORS_DIR = "src/flors"

# --- Завантаження макета карти ---
def load_map_layout(map_path):
    image = Image.open(map_path)
    width, height = image.size
    pixels = image.load()
    return pixels, width, height

# --- Завантаження всіх спрайтів у словник ---
def load_tile_images(directory):
    tile_images = {}
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            name = filename.replace(".png", "")
            path = os.path.join(directory, filename)
            image = pygame.image.load(path).convert_alpha()
            tile_images[name] = image
    return tile_images

# --- Створення всієї мапи ---
def generate_map(screen, pixels, width, height, walls, flors):
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            key = f"{r}_{g}_{b}"

            if r >= 200:
                image = walls.get(key)
            elif r >= 150:
                image = flors.get(key)
            else:
                image = None

            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

# --- Основна функція ---
def main():
    # Завантаження макету
    pixels, map_width, map_height = load_map_layout(MAP_PATH)

    # Визначення розмірів вікна
    screen_width = map_width * TILE_SIZE
    screen_height = map_height * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pygame Map Generator")

    # Завантаження текстур
    wall_tiles = load_tile_images(WALLS_DIR)
    flor_tiles = load_tile_images(FLORS_DIR)

    # Основний цикл
    running = True
    while running:
        screen.fill((0, 0, 0))  # Очистити екран

        generate_map(screen, pixels, map_width, map_height, wall_tiles, flor_tiles)

        pygame.display.flip()  # Оновлення екрану

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# --- Точка входу ---
if __name__ == "__main__":
    main()
