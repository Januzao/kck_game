import pygame
import sys

def main():
    pygame.init()

    # 1) Завантажуємо основне зображення
    image = pygame.image.load("photo.png")
    width, height = image.get_width(), image.get_height()

    # 2) Встановлюємо масштаб і створюємо вікно
    scale = 16
    screen = pygame.display.set_mode((width * scale, height * scale))
    pygame.display.set_caption("Заміна сірого пікселя картинкою")

    # 3) Завантажуємо замінну картинку з альфою і масштабуємо
    replace_img = pygame.image.load("c1c1c1f.png").convert_alpha()
    replace_img = pygame.transform.scale(replace_img, (scale, scale))

    # 4) Визначаємо точний відтінок сірого
    TARGET_GRAY = (193, 193, 193)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 5) Рендеримо кожен піксель
        for y in range(height):
            for x in range(width):
                color = image.get_at((x, y))
                rgb = (color.r, color.g, color.b)

                if rgb == TARGET_GRAY:
                    # тільки для #C1C1C1 — малюємо вашу картинку
                    screen.blit(replace_img, (x * scale, y * scale))
                else:
                    # для всіх інших — заливка початковим кольором
                    rect = pygame.Rect(x * scale, y * scale, scale, scale)
                    screen.fill(color, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
