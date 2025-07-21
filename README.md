# n_body_simulation
Simulates and displays an n-body system using Pygame.

Author: @ion727

## options

The following options can be either changed manually line 160 or enabled/disabled with command-line arguments.


`-n` *PLANETS*              --      number of planets to be simulated (recommended <200 on lower-end systems)

`-p` *digits* -- manually sets computational precision to *digits* digits (can lead to stuttering at high values), default is -1

`-P` -- enables Precise Mode, considerably improving simulation accuracy at the cost of animation smoothness

`--no_collision`    --      self-explanitory, collisions do not remove planets when True

`--stable`          --      planets begin with perfectly circular motion when True

`--sun`             --      one planet is replaced with a sun (800-1000 times heavier) when True

`--save` *FILE*      --      saves preferences to `preferences.txt` or FILE if specified

`--load` *FILE*            --      loads preferences from `preferences.txt` or FILE if specified

`--no_erase`         --   planets leave a permanent trail which can be erased with `t` keybind.

## controls
While the program is running, the following keys can be pressed to various effects:


`SPACE` -- display 1/5 of net gravitational force and velocity (toggle) as well as all planets' locations (1/5 to avoid covering the entire screen)

`p`     -- pause and unpause simulation

`t`     -- show/delete & hide planet trails (toggle)

`r`     -- half all planet's velocities

## preferences.txt
The following additional settings can be set to 1 (True) or 0 (False) in the `preferences.txt` file manually. Any flags used as command-line arguments override `preferences.txt`.

`info_toggle` -- displays/hides planet velocity (yellow) and net gravitational force (red)

`trail_toggle` -- shows/hides each planet's past positions.