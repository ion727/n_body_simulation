# n_body_simulation
Simulates and then displays an n-body system using Pygame.

To select the following options, please find line 141 the following information:

`n               --      number of planets to be simulated (recommended <200 on lower-end systems)`
`no_collision    --      self-explanitory, collisions do not remove planets when True`
`stable          --      planets begin with perfectly circular motion (subject to lose balance depending on computational accuracy) when True`
`sun             --      one planet is replaced with a sun (800-1000 times heavier) when True`
``
`system = System(n=3, HEIGHT, WIDTH, no_collision=False, stable=False, sun=False)`