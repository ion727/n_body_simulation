# n_body_simulation
Simulates and then displays an n-body system using Pygame.

## options

To select the following options, please find line 141 the following information:


`n`               --      number of planets to be simulated (recommended <200 on lower-end systems)

`no_collision`    --      self-explanitory, collisions do not remove planets when True

`stable`          --      planets begin with perfectly circular motion (subject to lose balance depending on computational accuracy) when True

`sun`             --      one planet is replaced with a sun (800-1000 times heavier) when True

`system` = System(n=3, HEIGHT, WIDTH, no_collision=False, stable=False, sun=False)

## controls
While the program is running, the following keys can be pressed to various effects:


`SPACE` -- display net gravitational force and velocity (toggle)

`p`     -- pause and unpause simulation

`t`     -- show/hide planet trails (toggle)

`r`     -- half all planet's velocities

## preferences.txt
The following settings can be set to 1 (True) or 0 (False) in the `preferences.txt` file manually. Any toggle updated during the simulation's runtime will automatically be saved to `preferences.txt`.

`info_toggle` -- displays/hides planet velocity (yellow) and net gravitational force (red)

`trail_toggle` -- shows/hides each planet's past positions.