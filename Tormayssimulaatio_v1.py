"""

"""

import pygame
import numpy as np

class Particle:
    def __init__(self, mass=1, pos=[0, 0], vel=[0, 0], colour=pygame.Color("orange"), radius=0.5):
        self.mass = mass
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array([0, 0])

        self.colour = colour
        self.radius = radius

        self.pos_new = self.pos
        self.vel_new = self.vel
        self.acc_new = self.acc

    def draw(self, env):
        centre = env.env_to_screen(*self.pos.tolist())
        size = self.radius * env.scale
        pygame.draw.circle(env.screen, self.colour, centre, size)

    def update( self):
        self.pos = self.pos_new
        self.vel = self.vel_new


class Environment:
    def __init__(self, screen):
        self.screen = screen

        self.width_pixels = self.screen.get_width()
        self.height_pixels = self.screen.get_height()
        self.width = 10
        self.scale = self.width_pixels / self.width
        self.height = self.height_pixels / self.scale

        self.g = np.array([0, -10])*0
        self.particles = []
        self.dt = 0.01

        self.integration_method = "Verlet"

        self.collision_tolerance = 1e-2
        self.collision_velocity_tolerance = 1e-2

    def euler(self, dt):
        for p in self.particles:
            p.acc = self.g
            p.pos_new += p.pos + dt * p.vel
            p.vel_new += p.vel + dt * p.acc

    def verlet(self, dt):
        for p in self.particles:
            p.acc = self.g
            p.pos_new = p.pos + dt * p.vel + 0.5 * dt**2 * p.acc
            p.vel_new = p.vel + dt * p.acc
            p.acc_new = self.g
            p.vel_new = p.vel + dt * (p.acc + p.acc_new) / 2

    def integrate(self, dt):
        if self.integration_method == "Euler":
            self.euler(dt)
        else:
            self.verlet(dt)


    def step(self, dt):
        self.integrate(dt)
        boundary_collisions = self.check_boundary_collisions()
        particle_collisions = self.check_particle_collisions()
        collisions = len(boundary_collisions) + len(particle_collisions)

        if not collisions:
            for p in self.particles:
                p.update()
            return dt

        else:
            t_a = 0
            t_b = dt
            for _ in range(5):
                dt = (t_b - t_a) / 2
                t_c = (t_a + t_b) / 2

                self.integrate(dt)

                boundary_collisions_new = self.check_boundary_collisions()
                particle_collisions_new = self.check_particle_collisions()
                collisions_new = len(boundary_collisions_new) + len(particle_collisions_new)
                # Jos törmäyksiä ei tapahdu, poistutaan silmukasta 
                if not collisions_new:
                    t_a = t_c
                    for p in self.particles:
                        p.update()
                else:
                    t_b = t_c
                    # Päivitetään lista törmäävistä kappaleista
                    boundary_collisions = boundary_collisions_new
                    particle_collisions = particle_collisions_new
            
            # Reagoidaan törmäyksiin
            self.resolve_boundary_collisions(boundary_collisions)
            self.resolve_particle_collisions(particle_collisions)

            # Päivitetään paikat ja nopeudet
            for p in self.particles:
                p.update()

        # Palautetaan aika, joka mentiin eteenpäin
        return t_b

    def update(self):
        t = 0
        while t < self.dt:
            t += self.step(self.dt - t)
    # Tarkistetaan, mitkä kappaleista törmäävät seiniin (siis ikkunan reunoihin)
    def check_boundary_collisions(self):
        colliding_particles = []

        for p in self.particles:
            
            dist_right = p.pos_new[0] + p.radius - self.width / 2

            dist_left = -p.pos_new[0] + p.radius - self.width / 2

            dist_top = p.pos_new[1] + p.radius - self.height / 2

            dist_bottom = -p.pos_new[1] + p.radius - self.height / 2

            if dist_right > self.collision_tolerance and p.vel_new[0] > self.collision_velocity_tolerance:
                colliding_particles.append((p, np.array([1, 0]), dist_right))

            if dist_left > self.collision_tolerance and p.vel_new[0] < -self.collision_velocity_tolerance:
                colliding_particles.append((p, np.array([-1, 0]), dist_left))

            if dist_top > self.collision_tolerance and p.vel_new[1] > self.collision_velocity_tolerance:
                colliding_particles.append((p, np.array([0, 1]), dist_top))
            
            if dist_bottom > self.collision_tolerance and p.vel_new[1] < -self.collision_velocity_tolerance:
                colliding_particles.append((p, np.array([0, -1]), dist_bottom))

        return colliding_particles

    def resolve_boundary_collisions(self, colliding_particles):
        coeff_of_rest = 0.8

        for p, n, d in colliding_particles:
            vel_rel = np.dot(p.vel_new, n)
            if abs(vel_rel) < self.collision_velocity_tolerance:
                p.vel_new -= vel_rel * n
                p.pos_new -= d * n

            else:
                p.vel_new -= (1 + coeff_of_rest) * vel_rel * n


    def check_particle_collisions(self):
        colliding_particles = []

        num_particles = len(self.particles)

        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                p_1 = self.particles[i]
                p_2 = self.particles[j]

                rel_pos = p_2.pos_new - p_1.pos_new
                dist = np.linalg.norm(rel_pos)
                normal = rel_pos / dist

                dist -= p_1.radius + p_2.radius
                rel_vel = np.dot(p_2.vel_new - p_1.vel_new, normal)

                if dist < -self.collision_tolerance and rel_vel < -self.collision_velocity_tolerance:
                    colliding_particles.append((p_1, p_2, normal, dist))

        return colliding_particles

    def resolve_particle_collisions(self, colliding_particles):
        coeff_of_rest = 0.8
        for p_1, p_2, normal, dist in colliding_particles:
            rel_vel = np.dot(p_2.vel_new - p_1.vel_new, normal)
            if abs(rel_vel) < self.collision_velocity_tolerance:
                p_1.pos_new += dist * normal / 2
                p_2.pos_new -= dist * normal / 2

            p_1.vel_new += (1 + coeff_of_rest) * rel_vel / (1 + p_1.mass / p_2.mass) * normal
            p_2.vel_new -= (1 + coeff_of_rest) * rel_vel / (1 + p_2.mass / p_1.mass) * normal

    def draw(self):
        self.screen.fill(pygame.Color("white"))
        for p in self.particles:
            p.draw(self)

    def env_to_screen(self, x, y):
        x_screen = self.scale * x + self.width_pixels / 2
        y_screen = -self.scale * y + self.height_pixels /2

        return x_screen, y_screen

    def screen_to_env(self, x_screen, y_screen):
        x = (x_screen - self.width_pixels / 2) / self.scale
        y = -(y_screen - self.height_pixels / 2) / self.scale

        return x, y

    def add_particle(self, pos, vel=[0, 0], mass=1, radius=0.5):
        self.check_overlap(Particle(mass=mass, pos=pos, vel=vel, radius=radius))

    def add_particle2(self, pos, vel=[0, 0], mass=2, radius=0.25):
        self.check_overlap(Particle(mass=mass, pos=pos, vel=vel, radius=radius))

    def check_overlap(self, p_new):
        dist_right = p_new.pos_new [0] + p_new.radius - self.width / 2
        dist_left = -p_new.pos_new [0] + p_new.radius - self.width / 2
        dist_top = p_new.pos_new [1] + p_new.radius - self.height / 2
        dist_bottom = -p_new.pos_new [1] + p_new.radius - self.width / 2

        if dist_right > 0:
            return
        if dist_left > 0:
            return
        if dist_top > 0:
            return
        if dist_bottom > 0:
            return
        
        if len(self.particles) >= 1:
            for p in self.particles:
                rel_pos = p.pos_new - p_new.pos_new
                dist = np.linalg.norm(rel_pos)

                dist -= p.radius + p_new.radius

                if dist < 0:
                    return
        self.particles.append(p_new)

# Alustetaan Pygame
pygame.init()

# Ruudun leveys ja korkeus
width, height = 800, 600

# Luodaan ikkuna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paska peli")

# Luodaan kello
fps = 60
clock = pygame.time.Clock()


# Luodaan ympäristö
env = Environment(screen)


# Pelisilmukka
running = True
while running:
    # käsitellään tapahtumat
    for event in pygame.event.get():
        # Jos painetaan ruksia, poistutaan silmukasta ja suljetaan ohjelma
        if event.type == pygame.QUIT:
            running = False

        # Jos klikataan hiirellä, lisätään kappale
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_screen_start, y_screen_start = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x_screen_end, y_screen_end = event.pos
            v_x = (x_screen_start - x_screen_end) * 0.03
            v_y = -(y_screen_start - y_screen_end) * 0.03
            x, y = env.screen_to_env(x_screen_start, y_screen_start)
            env.add_particle([x, y], [v_x, v_y])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x_screen_start, y_screen_start = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            x_screen_end, y_screen_end = event.pos
            v_x = (x_screen_start - x_screen_end) * 0.03
            v_y = -(y_screen_start - y_screen_end) * 0.03
            x, y = env.screen_to_env(x_screen_start, y_screen_start)
            env.add_particle2([x, y], [v_x, v_y])

    dt = clock.tick(fps)
    env.dt = dt / 1000
    
    # Päivitetään kaikkien objektien  paikat ja nopeudet
    env.update()

    # Päivitetään ruutu
    env.draw()
    pygame.display.update()
    