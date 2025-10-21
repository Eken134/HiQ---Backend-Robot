# robot.py
# Innehåller själva kärnan av simuleringen: världen och roboten.


class World:
    """En kvadratisk värld där roboten får röra sig."""
    def __init__(self, size: int = 5) -> None:
        if size <= 0:
            raise ValueError("Världens storlek måste vara positiv.")
        self.size = size

    def in_bounds(self, x: int, y: int) -> bool:
        """Returnerar True om (x, y) ligger inom världens gränser."""
        return 0 <= x < self.size and 0 <= y < self.size


class State:
    """Beskriver robotens läge – position (x, y) och riktning."""
    DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]

    # Varje riktning motsvarar en rörelse i (dx, dy)
    STEP = {
        "NORTH": (0, 1),
        "EAST":  (1, 0),
        "SOUTH": (0, -1),
        "WEST":  (-1, 0),
    }

    def __init__(self, x: int = 0, y: int = 0, facing: str = "NORTH") -> None:
        if facing not in self.DIRECTIONS:
            raise ValueError(f"Ogiltig riktning: {facing}")
        self.x = x
        self.y = y
        self.facing = facing

    # ---- Rörelser och rotationer ----
    def left(self) -> None:
        """Rotera åt vänster."""
        i = self.DIRECTIONS.index(self.facing)
        self.facing = self.DIRECTIONS[(i - 1) % 4]

    def right(self) -> None:
        """Rotera åt höger."""
        i = self.DIRECTIONS.index(self.facing)
        self.facing = self.DIRECTIONS[(i + 1) % 4]

    def next_xy(self) -> tuple[int, int]:
        """Beräkna nästa ruta i den riktning roboten tittar."""
        dx, dy = self.STEP[self.facing]
        return self.x + dx, self.y + dy

    def move_if_valid(self, world: World) -> bool:
        """Flytta framåt om det är tillåtet."""
        nx, ny = self.next_xy()
        if world.in_bounds(nx, ny):
            self.x, self.y = nx, ny
            return True
        return False


class Robot:
    """Robot som rör sig i sin värld."""
    def __init__(self, world: World) -> None:
        self.world = world
        self.state: State | None = None  # roboten börjar "inte placerad"

    def place(self, x: int, y: int, facing: str) -> None:
        """Placera roboten på bordet i given position och riktning."""
        if facing not in State.DIRECTIONS:
            return  # ogiltig riktning – ignoreras
        if not self.world.in_bounds(x, y):
            return  # utanför världen – ignoreras
        self.state = State(x, y, facing)

    def move(self) -> None:
        """Flytta roboten ett steg framåt."""
        if self.state:
            self.state.move_if_valid(self.world)

    def left(self) -> None:
        """Rotera roboten åt vänster."""
        if self.state:
            self.state.left()

    def right(self) -> None:
        """Rotera roboten åt höger."""
        if self.state:
            self.state.right()

    def report(self) -> str | None:
        """Returnera robotens nuvarande position och riktning som text."""
        if not self.state:
            return None
        return f"{self.state.x},{self.state.y},{self.state.facing}"
