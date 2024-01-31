"""

"""

import pygame

class Particle:
    def __init__(self, m, x, y, k, L, colour, size):
        self.m = m
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.k = k
        self.L = L

        self.colour = colour
        self.size = size


    def draw(self, surface):
        pygame.draw.line(surface, self.colour, (self.x, 0), (self.x, self.y), 10)
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.size)


class Environment:
    def __init__(self, screen):
        self.screen = screen

        self.g = 10
        self.particles = []
        self.dt = 0.01

    def update(self):
        for p in self.particles:
            a_y = self.g - p.k/p.m * (p.y - p.L)
            p.y += self.dt * p.v_y
            p.v_y += self.dt * a_y

    def draw(self):
        self.screen.fill((255, 255, 255))
        for p in self.particles:
            p.draw(self.screen)

    def add_particle(self, x):
        self.particles.append(Particle(1, x, 150, 1, 200, (255, 0, 0), 10))

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

# Luodaan ympäristö
env = Environment(screen)

# Lisätään hiukkanen
env.add_particle(100)
env.add_particle(200)

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
    env.update()

    # Päivitetään ruutu
    env.draw()
    pygame.display.update()
    clock.tick(fps)