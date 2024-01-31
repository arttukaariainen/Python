"""
Testaillaan Pygame-kirjastoa.
"""

import pygame

# Alustetaan Pygame
pygame.init()

# Ruudun leveys ja korkeus
width, height = 800, 800

# Luodaan ikkuna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paska peli")

# Vaihdetaan ikkunan väri
screen.fill((255, 255, 255))

# Piirretään ympyrä
pygame.draw.circle(screen, (0, 0, 0), (width / 2, height / 2), 25)

# Piirretään viiva
pygame.draw.line(screen, (0, 255, 0), (width / 2, 0), (width / 2, height / 2), 10)

# Pelisilmukka
running = True
while running:
    # käsitellään tapahtumat
    for event in pygame.event.get():
        # Jos painetaan ruksia, poistutaan silmukasta ja suljetaan ohjelma
        if event.type == pygame.QUIT:
            running = False

        # Jos painetaan vasenta nuolinäppäintä, muutetaan taustaväriä
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                screen.fill((255, 0, 0))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                screen.fill((255, 255, 255))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                pygame.draw.circle(screen, (255, 255, 0), (width / 2, height / 2), 25)
    
    # Päivitetään kaikkien objektien  paikat ja nopeudet

    # Päivitetään ruutu
    pygame.draw.line(screen, (0, 255, 0), (width / 2, 0), (width / 2, height / 2), 10)
    #pygame.draw.circle(screen, (0, 0, 0), (width / 2, height / 2), 25)
    pygame.display.update()