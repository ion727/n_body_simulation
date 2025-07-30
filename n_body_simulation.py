'''
author: ion727
'''
from random import randint
import pygame
from mpmath import mp, mpf, sqrt, sin, cos, atan2, ceil, root
import argparse

class Constants:
    G = mpf("6.67430e-11")
    Simulation_Scale = mpf("7")
    mass_const = mpf(5e15)
    #@property
    def rand_mass():
        return randint(int(mpf("1.5")*Constants.mass_const),int(3*Constants.mass_const))

class Planet:
    def __init__(self, coords=(0,0), /, *, parent=None, index=None, sun=False):
        self.parent = parent
        self.x, self.y = mpf(coords[0]), mpf(coords[1])
        self.dx = self.dy = self.ax = self.ay = mpf(0)
        self.mass = mpf(Constants.rand_mass() if parent.stable is False else 3*Constants.mass_const)
        self.radius = max(int(ceil(mpf(40) / mpf(parent.n))), mpf(3))
        self.colour = (randint(100,255), randint(100,255), randint(100,255))
        self.index = index
        if sun is True:
            self.mass *= mpf(randint(800, 1000))
        self.removed = False
        self.expulsed = False
        self.trail = []
        self.is_sun = sun
        if sun:
            self.radius *= 3
    def init_velocities(self):
        self.dx =  self.ay*75 / root(self.parent.n,2)
        self.dy = -self.ax*75 / root(self.parent.n,2)
    def subtick(self, planet, d_time):
        """
        OUTPUT:
        0 -- updated successfully
        1 -- collision
        2 -- expulsion
        """
        # create expulsion bounding box
        if self.IsExpulsed:
            return 2

        dx = planet.x - self.x
        dy = planet.y - self.y
        r = sqrt(dx**2 + dy**2)
        if (r <= self.radius + planet.radius) and (self.parent.no_collision is False):
            return 1
        F = ((not self.parent.solar_system)*mpf(Constants.Simulation_Scale) + mpf(0.01)) * Constants.G * self.mass * planet.mass / r**2
        frac = F * mpf(d_time) / r
        delta_x = dx*frac
        delta_y = dy*frac
        self.ax += delta_x
        self.ay += delta_y
        self.dx += delta_x
        self.dy += delta_y
        return 0

    def update(self, d_time, trail_toggle, trail_length, no_erase):
        self.x += self.dx / self.mass * mpf(d_time)
        self.y += self.dy / self.mass * mpf(d_time)
        
        # raise error if complex numbers slip in
        if not isinstance(self.x, mpf) or not isinstance(self.y, mpf):
            raise ValueError(f"Error: Invalid position x={self.x}, y={self.y} for planet {self.index}")

    def update_trail(self, trail_length, no_erase):
        if not self.removed:
            self.trail.append((int(self.x), int(self.y)))
        else:
            if len(self.trail) != 0:
                self.trail.pop(0)
            return
        if no_erase is False and len(self.trail) > 300:
            self.trail.pop(0)
    def draw(self, surface, info_toggle, trail_toggle, speed_controller):        
        if not self.removed:
            pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), int(self.radius))
        if trail_toggle is True:
            if len(self.trail) > 1:
                width = int(ceil(self.radius/10))
                draw_lines = pygame.draw.lines if width > 1 else pygame.draw.aalines
                draw_lines(surface, self.colour, False, self.trail, width)
        if info_toggle is True:
            pygame.draw.line(surface, (200,0,0), 
                             (int(self.x), int(self.y)), 
                             (int(self.x + float(self.ax / self.mass * 10 / speed_controller)), 
                              int(self.y + float(self.ay / self.mass * 10 / speed_controller))), 3)
            pygame.draw.line(surface, (200,200,0), 
                             (int(self.x), int(self.y)), 
                             (int(self.x + float(self.dx / self.mass / 5)), 
                              int(self.y + float(self.dy / self.mass / 5))), 3)
    @property
    def IsExpulsed(self):
        h_WIDTH = self.parent.WIDTH // 2
        h_HEIGHT = self.parent.HEIGHT // 2
        return not ((-h_WIDTH < self.x < h_WIDTH*3) and (-h_HEIGHT < self.y < h_HEIGHT*3))
            


class System:
    def __str__(self):
        return "[" + "\n ".join([f"{planet.index}: ({int(planet.x)}, {int(planet.y)}), removed={planet.removed}" for planet in self.planets]) + "]\n"

    def __init__(self, WINDOW, HEIGHT, WIDTH, *, n, no_collision=False, stable=False, sun=False):
        self.WINDOW = WINDOW
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.r = min(HEIGHT, WIDTH) // 4
        self.n = n
        self.planets = []
        self.no_collision = no_collision
        self.solar_system = sun
        self.stable = stable
        self.paused = True

        for i in range(n):
            theta = mpf(2) * mp.pi * i / n  # Evenly spaced angle around circle
            x = mpf(self.WIDTH // 2) + self.r * cos(theta)
            y = mpf(self.HEIGHT // 2) + self.r * sin(theta)
            if i == 0 and sun is True:
                self.planets.append(Planet((x, y), parent=self, index=i, sun=True))
                continue
            self.planets.append(Planet((x, y), parent=self, index=i))
        self.init()
        
    def init(self):
        self.compute_planet_accels(mpf(1)/60)
        for planet in self.planets:
            planet.init_velocities()

    def compute_planet_accels(self, d_time=1/60):
        for current in self.remaining_planets:
            current.ax = mpf(0)
            current.ay = mpf(0)
            for planet in self.remaining_planets:
                if current is planet:
                    continue
                out=current.subtick(planet, d_time)
                if out == 1 and self.no_collision is False:
                    if not current.is_sun:
                        current.removed = True
                        #print(f"planet 1: {current.index}: COLLIDED. Remaining: {sum((int(planet.removed) for planet in self.planets))}")
                    if not planet.is_sun:
                        planet.removed = True
                    break
                elif out == 2:
                    current.removed = True
                    current.expulsed = True
                    break
    def draw_planets(self, info_toggle, trail_toggle, speed_controller):
        for planet in self.planets:
            planet.draw(self.WINDOW, info_toggle, trail_toggle, speed_controller)
    def update_trails(self, trail_length, no_erase):
        for planet in self.planets:
            planet.update_trail(trail_length, no_erase)
    def update_positions(self, d_time, trail_toggle, trail_length, no_erase):
        for planet in self.remaining_planets:
            planet.update(d_time, trail_toggle, trail_length, no_erase)
    def check_status(self):
        for planet in self.planets:
            planet.expulsed = planet.IsExpulsed
        if all((planet.removed for planet in self.planets)):
            self.paused = True
    @property
    def remaining_planets(self):
        return (planet for planet in self.planets if planet.removed is False)

def render_planet_info(surface, planets, font, alpha=200, x=10, y=10, spacing=4):
    lines = []
    for i, planet in enumerate(planets):
        text = f"{i+1:<2}| EXPULSED" if planet.expulsed else f"{i+1:<2}| COLLIDED" if planet.removed else f"{i+1:<2}| ({int(planet.x)}, {int(planet.y)})"
        lines.append(text)

    for k, line in enumerate(lines):
        text_surf = font.render(line, True, (255, 255, 255))
        text_surf = text_surf.convert_alpha()
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (x, y + k * (font.get_height() + spacing)))

def render_simulation_speed(surface, speed_controller, font, alpha=200, margin=10):
    speed_value = ceil(mpf(speed_controller) * 100) / 100
    text = f"Simulation speed: {float(speed_value):.2f}"
    text_surf = font.render(text, True, (255, 255, 255))
    text_surf = text_surf.convert_alpha()
    text_surf.set_alpha(alpha)

    surface_width = surface.get_width()
    x = surface_width - text_surf.get_width() - margin
    y = margin

    surface.blit(text_surf, (x, y))

def load_settings(load, **overrides):
    # default settings
    settings = {
        "n": 3,
        "precision" : -1,
        "trail_length" : 300,
        "precise_mode" : False,
        "no_collision": False,
        "stable": True,
        "sun": False,
        "no_erase":False
    }

    overriden_settings = {}
    # Find common keys
    common_keys = settings.keys() & overrides.keys()
    
    for key in common_keys:
        if settings[key] != overrides[key]:
            overriden_settings[key] = overrides[key]
    

    try:
        with open(load, "r") as fp:
            for line in fp:
                line = line.strip().rstrip(";")
                if (not line) or ("=" not in line):
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in settings:
                    if key in ("n","precision","trail_length"):
                        settings[key] = int(value)
                    else:
                        settings[key] = bool(int(value))
    except FileNotFoundError:
        raise FileNotFoundError("LOAD file not found.")

    for key, val in overriden_settings.items():
        if key not in settings:
            raise ValueError(f"Unexpected argument: {key}")
        settings[key] = val

    return (
        settings["n"],
        settings["precision"],
        settings["precise_mode"],
        settings["trail_length"],
        settings["no_collision"],
        settings["stable"],
        settings["sun"],
        settings["no_erase"]
    )

def main(n=2,
        *,
        precision=-1,
        trail_length=300,
        precise_mode=False,
        no_collision=False,
        stable=False,
        sun=False,
        save=None,
        load=None, 
        no_erase=False):

    info_toggle = False
    trail_toggle = True

    default_file = "preferences.txt"
    if load and type(load) is not str:
        load = default_file

    if load:
        n,            \
        precision,    \
        precise_mode, \
        trail_length, \
        no_collision, \
        stable,       \
        sun,          \
        no_erase =    \
        load_settings(load,
                    n=n, 
                    precision=precision, 
                    precise_mode=precise_mode, 
                    trail_length=trail_length,
                    no_collision=no_collision, 
                    stable=stable, 
                    sun=sun, 
                    no_erase=no_erase)

    if (type(precision) is not int) or (precision == -1):
        mp.dps = 2048 // n
    else:
        mp.dps = precision
    pygame.init()
    WIDTH = HEIGHT = 800
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Consolas", 12)
    pygame.display.set_caption("N-Body Simulation")
    clock = pygame.time.Clock()

    #### SYSTEM CREATION HERE ####
    system = System(WINDOW, HEIGHT, WIDTH, n=n, no_collision=no_collision, stable=stable, sun=sun)

    speed_controller = 1
    running = True
    
    while running:
        d_time = (clock.tick(60) / 1000.0) if precise_mode is False else mpf(0.003125)#*system.n
        d_time *= speed_controller
        WINDOW.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if save:
                    if type(save) is not str:
                        save = default_file
                    with open(save, "w") as fp:
                        fp.write( \
f"""n={len(system.planets)};
precision={int(precision)};
trail_length={int(trail_length)};
precise_mode={int(precise_mode)};
no_collision={int(no_collision)};
stable={int(stable)};
sun={int(sun)};
no_erase={int(no_erase)};""")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    info_toggle = not info_toggle
                if event.key == pygame.K_t:
                    trail_toggle = not trail_toggle
                    if trail_toggle is False:
                        for planet in system.planets:
                            planet.trail = []
                if event.key == pygame.K_p:
                    system.paused = not system.paused
                if event.key == pygame.K_r:
                    for planet in system.planets:
                        planet.dx /= 2
                        planet.dy /= 2
                # speed controller
                if event.key == pygame.K_UP:
                    speed_controller *= mpf("1.25")
                if event.key == pygame.K_DOWN:
                    speed_controller /= mpf("1.25")
        
        system.check_status()
        if not system.paused:
            # update before compute_planet_accels so that ax & ay dont become obsolete
            system.update_positions(d_time, trail_toggle, trail_length, no_erase)
            if trail_toggle:
                system.update_trails(trail_length, no_erase)
            system.compute_planet_accels(d_time)
        system.draw_planets(info_toggle, trail_toggle, speed_controller)
        
        if info_toggle:
            render_planet_info(WINDOW, system.planets, font)
        render_simulation_speed(WINDOW, speed_controller, font)
        pygame.display.update()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="A simple n-body simulation, check out ./README.md for more info."
)

    parser.add_argument(
        '-n', type=int, metavar='NUM', default=3,
        help="Creates NUM planets to be simulated (default: 3)."
    )

    parser.add_argument(
        '-p', type=int, metavar='NUM', default=-1,
        help="Manually sets computational precision to NUM digits (can cause stuttering). Default is -1 (2048 distributed across planets)."
    )

    parser.add_argument(
        '-t', type=int, metavar='NUM', default=300,
        help="Makes the trails NUM positions long (default: 300). Overridden by `-s`."
    )

    parser.add_argument(
        '-P',"--precise", action='store_true', default=False,
        help="Enables Precise Mode, increasing simulation precision by disregarding animation smoothness."
    )

    parser.add_argument(
        '--no_collision', action='store_true', default=False,
        help="Prevents colliding planets from being deleted."
    )

    parser.add_argument(
        '--stable', action='store_true', default=True,
        help="Makes planets' mass and starting velocities equal, leading to gravitational equilibrium."
    )

    parser.add_argument(
        '-s', '--sun', action='store_true', default=False,
        help="Selects a planet to be 800-1000 times heavier, acting like a sun."
    )

    parser.add_argument(
        '-E', '--no_erase', action='store_true', default=False,
        help="Planets leave a permanent trail which can be erased with the `t` key."
    )

    parser.add_argument(
        '--save',
        nargs='?', const='preferences.txt', default=None, metavar='FILE',
        help="Upon closing, save prefs to FILE or 'preferences.txt' if none provided."
    )

    parser.add_argument(
        '--load',
        nargs='?', const='preferences.txt', default=None, metavar='FILE',
        help="Load prefs from FILE, defaulting to 'preferences.txt' if none provided."
    )

    args = parser.parse_args()

    main(n=args.n,
        precision=args.p,
        trail_length=args.t,
        precise_mode=args.precise,
        no_collision=args.no_collision,
        stable=args.stable,
        sun=args.sun,
        save=args.save,
        load=args.load,
        no_erase=args.no_erase)
    