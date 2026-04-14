import curses

class Palette:
    """Handles color pair initialization for curses."""
    def __init__(self):
        curses.use_default_colors()
        # Pair ID, Foreground, Background (-1 is default terminal bg)
        curses.init_pair(1, curses.COLOR_YELLOW, -1) # Pacman
        curses.init_pair(2, curses.COLOR_RED, -1)    # Blinky
        curses.init_pair(3, curses.COLOR_CYAN, -1)   # Inky
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)# Pinky
        curses.init_pair(5, curses.COLOR_WHITE, -1)  # Items/Borders

class Scene:
    """The Renderer. It takes the game state and draws it."""
    def __init__(self, window, level, palette):
        self.window = window
        self.level = level
        self.points = 0
        self.life = 3
        self.standing_start_announcement = False
        self.death = False
        self.power_capsule = False
        self.flash = False

    def render(self):
        self.window.erase()
        
        # 1. Draw Map
        for y, row in enumerate(self.level.pmap.grid):
            for x, char in enumerate(row):
                self.window.addch(y, x, char, curses.color_pair(5))

        # 2. Draw Pacman
        p = self.level.pacman
        self.window.addch(p.y, p.x, p.symbol, curses.color_pair(1))

        # 3. Draw Ghosts
        for i, g in enumerate(self.level.ghosts):
            color = curses.color_pair(i + 2)
            char = g.symbol
            if self.power_capsule:
                char = 'ᗣ' # Scared ghost
                color = curses.color_pair(3) if not self.flash else curses.color_pair(5)
            self.window.addch(g.y, g.x, char, color)

        # 4. Draw UI
        self.window.addstr(0, self.level.pmap.width + 2, f"SCORE: {self.points}")
        self.window.addstr(1, self.level.pmap.width + 2, f"LIVES: {'❤' * self.life}")
        
        if self.standing_start_announcement:
            self.window.addstr(self.level.pmap.height // 2, 
                               self.level.pmap.width // 2 - 3, "READY!", curses.A_BOLD)

        self.window.refresh()
