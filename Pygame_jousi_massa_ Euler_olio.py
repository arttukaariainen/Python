"""
Testaillaan Pygame-kirjastoa.
"""

import pygame

class Particle:
    def __init__(self, m, x, y, k, L, g, colour, size):
        self.m = m
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.k = k
        self.L = L
        self.g = g

        self.colour = colour
        self.size = size

    def update(self, dt):
        a_y = self.g - self.k/self.m * (self.y - self.L)
        self.y += dt * self.v_y
        self.v_y += dt * a_y

    def draw(self, surface):
        pygame.draw.line(surface, self.colour, (self.x, 0), (self.x, self.y), 10)
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.size)



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

# Aika-askel
dt = 0.01

# Vaihdetaan ikkunan väri
screen.fill((255, 255, 255))

# Luodaan hiukkanen
# m, x, y, k, L, colour, size
hiukkanen = Particle(1, 100, 200, 1, 150, 10, (255, 0, 0), 20)
hiukkanen_2 = Particle(2, 300, 200, 1, 150, 10, (0, 0, 255), 10)

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
    hiukkanen.update(dt)
    hiukkanen_2.update(dt)

    # Päivitetään ruutu
    screen.fill((255, 255, 255))
    hiukkanen.draw(screen)
    hiukkanen_2.draw(screen)
    pygame.display.update()
    clock.tick(fps)