'''
author: ion727
date of completion: 13/07/2025
'''

import random
import math
import pygame

class Planet:
    def __init__(self, coords=(0,0), /, *, mass = random.randint(200000,300000), parent=None, index=None, stable=False, sun=False):
        self.x, self.y = coords
        self.ax = self.ay = 0
        self.mass = mass
        self.radius = 5 if stable is False else 1
        self.colour = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
        self.index = index
        if sun is True:
            self.mass *= random.randint(800, 1000)
        self.parent = parent
        self.collided = False
        self.trail = []

        theta = math.atan2(self.y - parent.HEIGHT / 2, self.x - parent.WIDTH / 2)
        speed = mass*random.uniform(50, 52 if stable is False else 50)
        self.dx = -math.sin(theta) * speed
        self.dy =  math.cos(theta) * speed

        if self.index != parent.n - 1:
            self.parent.initial_velocities_x.append(self.dx)
            self.parent.initial_velocities_y.append(self.dy)
        else:
            self.dx = -sum(self.parent.initial_velocities_x)
            self.dy = -sum(self.parent.initial_velocities_y)

        
    def subtick(self, planet):
        """
        OUTPUT:
        0 -- updated successfully
        1 -- collision

        """
        r = math.dist((self.x, self.y), (planet.x, planet.y))
        if r <= self.radius + planet.radius:
            return 1
        F = Constants.Simulation_Speed*Constants.G*self.mass*planet.mass/r**2
        self.ax += F*(planet.x - self.x)/r/self.parent.not_collided
        self.ay += F*(planet.y - self.y)/r/self.parent.not_collided
        self.dx += F*(planet.x - self.x)/r/self.parent.not_collided
        self.dy += F*(planet.y - self.y)/r/self.parent.not_collided
        return 0
    def update(self, d_time):
        self.x += self.dx / self.mass * d_time
        self.y += self.dy / self.mass * d_time
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 75:
            self.trail.pop(0)
    def draw(self, surface, info_toggle, trail_toggle):        
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), self.radius)
        if trail_toggle is True:
            for pos in self.trail:
                pygame.draw.circle(surface, self.colour, pos, 1)
        if info_toggle is True:
            pygame.draw.line(surface, (255,0,0), (int(self.x), int(self.y)), (int(self.x + self.ax/self.mass*100), int(self.y+self.ay/self.mass*100)), 3)
            pygame.draw.line(surface, (255,255,0), (int(self.x), int(self.y)), (int(self.x + self.dx/self.mass), int(self.y+self.dy/self.mass)), 3)

class System:
    def __str__(self):
        return "[" + "\n ".join([f"{planet.index}: ({int(planet.x)}, {int(planet.y)}), collided={planet.collided}" for planet in self.planets]) + "]\n"
    def __init__(self, n, HEIGHT, WIDTH, no_collision=False, stable=False):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.r = min(HEIGHT,WIDTH) // 4
        self.n = n
        self.not_collided = n
        self.planets = []
        self.initial_velocities_x = []
        self.initial_velocities_y = []
        self.no_collision = no_collision
        for i in range(n):
            theta = 2 * math.pi * i / n  # Evenly spaced angle around circle
            if i == 0:
                self.planets.append(Planet((self.WIDTH // 2 + self.r*math.cos(theta), self.HEIGHT // 2 + self.r*math.sin(theta)), parent=self, index=i, stable=stable, sun=True))
                continue
            self.planets.append(Planet((self.WIDTH // 2 + self.r*math.cos(theta), self.HEIGHT // 2 + self.r*math.sin(theta)), parent=self, index=i, stable=stable))
    def tick(self, d_time):
        for current in self.planets:
            if current.collided == 1:
                continue
            current.ax = 0
            current.ay = 0
            for planet in self.planets:
                if current is planet or planet.collided is True:
                    continue
                if current.subtick(planet) == 1 and self.no_collision is False:
                    current.collided = True
                    planet.collided = True
                    self.not_collided -= 2
                    break
        for planet in self.planets:
            if planet.collided:
                continue
            planet.update(d_time)

class Constants:
    G = 6.67430e-11
    Simulation_Speed = 7000000000

def render_planet_info(surface, planets, font, alpha=200, x=10, y=10, spacing=4):
    lines = []
    for i, planet in enumerate(planets):
        text = f"{i+1:<2}| COLLIDED" if planet.collided else f"{i+1:<2}| ({int(planet.x)}, {int(planet.y)})"
        lines.append(text)

    for k, line in enumerate(lines):
        text_surf = font.render(line, True, (255, 255, 255))
        text_surf = text_surf.convert_alpha()
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (x, y + k * (font.get_height() + spacing)))


def main():
    pygame.init()
    WIDTH = HEIGHT = 800
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Consolas", 12)
    pygame.display.set_caption("N-Body Simulation")
    clock = pygame.time.Clock()
    running = True
    info_toggle = False
    trail_toggle = True
    paused = True
    ######## CONTROL CENTER ########
    '''
    n               --      number of planets to be simulated (recommended <200 on lower-end systems)
    no_collision    --      self-explanitory, collisions do not remove planets when True
    stable          --      planets begin with perfectly circular motion (subject to lose balance depending on computational accuracy) when True
    sun             --      one planet is replaced with a sun (800-1000 times heavier) when True
    '''
    system = System(n=3, HEIGHT, WIDTH, no_collision=False, stable=False, sun=False)
    while running:
        d_time = clock.tick(60) / 1000.0
        WINDOW.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    info_toggle = not info_toggle
                if event.key == pygame.K_t:
                    trail_toggle = not trail_toggle
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    for planet in system.planets:
                        planet.dx /= 2
                        planet.dy /= 2
        for planet in system.planets:
            if planet.collided:
                continue
            planet.draw(WINDOW, info_toggle, trail_toggle)
        if not paused:
            system.tick(d_time)
        render_planet_info(WINDOW, system.planets, font)
        pygame.display.update()

main()