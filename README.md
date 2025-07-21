# n_body_simulation
Simulates and displays an n-body system using Pygame.

Author: @ion727

## options

The following options can be either changed manually line 160 or enabled/disabled with command-line arguments.


`-n` *PLANETS*              --      number of planets to be simulated (recommended <200 on lower-end systems)

`--no_collision`    --      self-explanitory, collisions do not remove planets when True

`--stable`          --      planets begin with perfectly circular motion when True

`--sun`             --      one planet is replaced with a sun (800-1000 times heavier) when True

`--save` *FILE*      --      saves preferences to `preferences.txt` or FILE if specified

`--load` *FILE*            --      loads preferences from `preferences.txt` or FILE if specified

`--no_erase`         --   planets leave a permanent trail which can be erased with `t` keybind.

`-p` *digits* -- manually sets computational precision to *digits* digits (can lead to stuttering at high values), default is -1
## controls
While the program is running, the following keys can be pressed to various effects:


`SPACE` -- display net gravitational force and velocity (toggle) as well as all planets' locations

`p`     -- pause and unpause simulation

`t`     -- show/hide planet trails (toggle)

`r`     -- half all planet's velocities

## preferences.txt
The following settings can be set to 1 (True) or 0 (False) in the `preferences.txt` file manually. Any toggle updated during the simulation's runtime will automatically be saved to `preferences.txt` if `--save_prefs` is used and can be loaded using --load

`info_toggle` -- displays/hides planet velocity (yellow) and net gravitational force (red)

`trail_toggle` -- shows/hides each planet's past positions.