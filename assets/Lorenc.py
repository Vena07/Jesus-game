import os
import sys
import pygame

# Inicializace Pygame
pygame.init()
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jesus / Žiba Game - Asset Visualizer")

# Dynamická cesta ke složce se skriptem
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_PATH = os.path.join(
    SCRIPT_DIR, "player.png"
)  # Sem vlož PNG postavy (Jesus/Žiba)

# Načtení PNG postavy s průhledností
try:
    player_image = pygame.image.load(PLAYER_PATH).convert_alpha()
    player_image = pygame.transform.scale(player_image, (60, 80))
    player_loaded = True
except (pygame.error, FileNotFoundError):
    print(
        f"Upozornění: Soubor 'player.png' nebyl nalezen ve složce: {SCRIPT_DIR}"
    )
    print("Zobrazuje se náhradní grafická postava.")
    player_loaded = False

# Definice barevného tématu
COLOR_SKY_TOP = (135, 206, 250)  # Světle modrá obloha
COLOR_SKY_BOTTOM = (240, 248, 255)  # Nebeská běloba
COLOR_CLOUD = (255, 255, 255, 200)  # Bílé mraky
COLOR_GROUND = (76, 153, 0)  # Trávník
COLOR_DIRT = (102, 51, 0)  # Hlína
COLOR_PLATFORM = (160, 82, 45)  # Dřevěná/kamenná plošina
COLOR_GOLD = (255, 215, 0)  # Zlatá mince
COLOR_GOLD_SHINE = (255, 247, 153)  # Lesk mince

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. POZADÍ (Nebeský přechod / Gradient)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(COLOR_SKY_TOP[0] * (1 - ratio) + COLOR_SKY_BOTTOM[0] * ratio)
        g = int(COLOR_SKY_TOP[1] * (1 - ratio) + COLOR_SKY_BOTTOM[1] * ratio)
        b = int(COLOR_SKY_TOP[2] * (1 - ratio) + COLOR_SKY_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    # Dekorativní mraky na pozadí
    pygame.draw.circle(screen, (255, 255, 255), (150, 80), 40)
    pygame.draw.circle(screen, (255, 255, 255), (190, 70), 50)
    pygame.draw.circle(screen, (255, 255, 255), (230, 80), 40)

    pygame.draw.circle(screen, (255, 255, 255), (600, 120), 35)
    pygame.draw.circle(screen, (255, 255, 255), (635, 110), 45)

    # 2. ZEMĚ A PLOŠINY
    # Hlavní zem
    pygame.draw.rect(screen, COLOR_DIRT, (0, 380, WIDTH, 70))
    pygame.draw.rect(screen, COLOR_GROUND, (0, 380, WIDTH, 15))

    # Levá plošina
    pygame.draw.rect(screen, COLOR_PLATFORM, (200, 280, 140, 20))
    pygame.draw.rect(screen, (100, 40, 20), (200, 280, 140, 20), 3)

    # Pravá vyšší plošina
    pygame.draw.rect(screen, COLOR_PLATFORM, (480, 200, 160, 20))
    pygame.draw.rect(screen, (100, 40, 20), (480, 200, 160, 20), 3)

    # 3. MINCE (Sběratelné assety)
    coin_positions = [(230, 250), (270, 250), (310, 250), (530, 170), (580, 170)]
    for cx, cy in coin_positions:
        pygame.draw.circle(screen, COLOR_GOLD, (cx, cy), 12)
        pygame.draw.circle(screen, (218, 165, 32), (cx, cy), 12, 2)  # Okraj
        pygame.draw.circle(
            screen, COLOR_GOLD_SHINE, (cx - 3, cy - 3), 3
        )  # Detail lesku

    # 4. POSTAVA (Jesus / Žiba - PNG Asset)
    if player_loaded:
        # Vykreslení načteného PNG na první plošině
        screen.blit(player_image, (240, 200))
    else:
        # Zástupný grafický objekt, pokud PNG chybí
        pygame.draw.rect(screen, (230, 126, 34), (250, 200, 40, 80), border_radius=8)
        pygame.draw.circle(screen, (241, 196, 15), (270, 190), 15)  # Svatozář/Detail

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()