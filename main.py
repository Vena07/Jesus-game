import sys
import pygame

# Inicializace Pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Angry Birds - Asset Visualizer")

# Načtení PNG prasete (nahraďte 'pig.png' cestou k vašemu souboru)
# Pro snadnou výměnu stačí změnit název souboru v tomto řádku
PIG_PATH = "pig.png"

try:
    pig_image = pygame.image.load(PIG_PATH).convert_alpha()
    # Změna velikosti prasete podle potřeby (např. 50x50 px)
    pig_image = pygame.transform.scale(pig_image, (50, 50))
    pig_loaded = True
except pygame.error:
    print(
        f"Soubor '{PIG_PATH}' nebyl nalezen. Zobrazí se zástupný zelený kruh."
    )
    pig_loaded = False

# Hlavní smyčka pro vykreslení grafiky (bez fyziky/logiky)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Pozadí (Obloha)
    screen.fill((135, 206, 235))

    # 2. Zeme a tráva
    pygame.draw.rect(screen, (139, 90, 43), (0, 350, 800, 50))  # Hlína
    pygame.draw.rect(screen, (38, 139, 7), (0, 350, 800, 15))  # Tráva

    # 3. Prak (Zástupný asset)
    pygame.draw.rect(screen, (92, 64, 51), (150, 260, 15, 90))
    pygame.draw.rect(screen, (92, 64, 51), (135, 240, 15, 30))
    pygame.draw.rect(screen, (92, 64, 51), (165, 240, 15, 30))

    # 4. Pták (Zástupný asset)
    pygame.draw.circle(screen, (231, 76, 60), (140, 245), 16)

    # 5. Dřevěná bedna (Zástupný asset)
    pygame.draw.rect(screen, (211, 84, 0), (600, 270, 80, 80))
    pygame.draw.rect(screen, (110, 44, 0), (600, 270, 80, 80), 3)

    # 6. PRASE (Vykreslení PNG obrázku)
    if pig_loaded:
        # Vykreslení načteného PNG na pozici nad bednou (x=615, y=220)
        screen.blit(pig_image, (615, 220))
    else:
        # Zástupný kruh, pokud PNG chybí
        pygame.draw.circle(screen, (46, 204, 113), (640, 245), 25)

    pygame.display.flip()

pygame.quit()
sys.exit()