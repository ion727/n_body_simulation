# N-Body Simulation

A 2D gravitational n-body simulator with real-time visualization and high-precision physics.

---

## Author

`ion727`

---

## Overview

This Python program simulates gravitational interactions between multiple celestial bodies (planets) in two-dimensional space. It models orbital mechanics, collisions, and dynamic behaviors of planetary systems with an emphasis on numerical accuracy and visual clarity.

Key features include:
- Arbitrary number of planets
- High-precision gravitational computations using `mpmath`
- Real-time animation using `pygame`
- Optional central "sun" body with greater mass
- Configurable stability, collisions, and trail visualization
- Toggleable on-screen information and velocity/acceleration vectors
- Saving/loading of simulation preferences

---


## Command Line Arguments

| Option                | Description                                                                                          | Default           |
|-----------------------|------------------------------------------------------------------------------------------------------|-------------------|
| `-n NUM`              | Number of planets to simulate                                                                         | `3`               |
| `-p NUM`              | Set precision (in digits). `-1` distributes 2048 digits across planets                                | `-1`              |
| `-t NUM`              | Length of trail history (number of recorded positions)                                               | `300`             |
| `-P`, `--precise`     | Enable precise mode: prioritizes accuracy over animation smoothness                                  | Off               |
| `--no_collision`      | Disable removal of planets upon collision                                                            | Off               |
| `--stable`            | Initialize planets with equal mass and orbital velocities (stable orbits)                            | On                |
| `-s`, `--sun`         | Designate one planet as a "sun" with 800–1000× more mass                                              | Off               |
| `-E`, `--no_erase`    | Make planet trails permanent (can be cleared with the `t` keybind)                                        | Off               |
| `--save [FILE]`       | Save current settings to a file on exit (default: `preferences.txt`)                                 | Off               |
| `--load [FILE]`       | Load simulation settings from a file before starting (default: `preferences.txt`)                    | Off               |

---

## In-Simulation Controls

| Key        | Action                                                                          |
|------------|----------------------------------------------------------------------------------|
| `Space`    | Toggle display of acceleration and velocity vectors as well as planet positions & status               |
| `T`        | Toggle trails on/off (clears trails when turned off)                            |
| `P`        | Pause or resume the simulation                                                  |
| `R`        | Halve all planet velocities (slow the system down)                              |
| `↑` / `↓`  | Increase or decrease simulation speed                                            |
| `ESC` / Close window | Exit simulation                                                       |

---

## preferences.txt

The `preferences.txt` file is an optional configuration file that stores simulation settings between runs.

If you run the program with the `--save` flag, the current simulation settings will be written to `preferences.txt` (or to a specified file). These settings will be automatically loaded on the next run if the `--load` flag is provided.
