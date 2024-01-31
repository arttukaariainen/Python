"""
Testaillaan Pygame-kirjastoa.
"""

import pygame

# Fysikaaliset parametrit
g = 10
k = 1
m = 1
L = 100

# Alustetaan Pygame
pygame.init()

# Ruudun leveys ja korkeus
width, height = 400, 300

# Luodaan ikkuna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paska peli")

# Luodaan kello
fps = 60
clock = pygame.time.Clock()

# Alkuarvot
x_0 = width / 2
y_0 = height / 2
v_x_0 = 0
v_y_0 = 0

# Aika-askel
dt = 0.01

# Alustetaan muuttujat
x = x_0
y = y_0
v_x = v_x_0
v_y = v_y_0

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
    
    # Päivitetään kaikkien objektien  paikat ja nopeudet
    a_x = 0
    a_y = g - k/m * (y - L) - 0.2 * v_y

    x += dt * v_x + 0.5 * dt**2 * a_x
    y += dt * v_y + 0.5 * dt**2 * a_y

    v_y_new = v_y * dt * a_y
    a_y_new = g - k/m * (y - L) - 0.2 * v_y_new

    v_y += dt * a_y
    v_x += dt * a_x * (a_y + a_y_new)/2

    # Päivitetään ruutu
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 255, 0), (x, 0), (x, y), 10)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 25)
    pygame.display.update()
    clock.tick(fps)