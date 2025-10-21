# simulator.py
# Enkel körbar “simulator” för roboten.
# Läser en textfil med kommandon och skriver ut alla REPORT-rader.

import sys
from robot import World, Robot


def read_place_string(line: str):
    """
    Plockar ut (x, y, facing) rader som börjar med PLACE.|Returnerar None om den inte går att tolka.
    """
    s = line.strip()
    if not s.upper().startswith("PLACE"):
        return None

    # Ta bort själva ordet "PLACE" och ev. inledande komma
    rest = s[5:].strip()
    if rest.startswith(","):
        rest = rest[1:]

    parts = [p.strip() for p in rest.split(",")]
    if len(parts) != 3:
        return None

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        return None

    facing = parts[2].upper()
    return x, y, facing


def run_instructions(lines):
    """
    Kör en sekvens av textkommandon och returnerar alla REPORT-rader i ordning.
    Ignorerar:
      - tomma rader
      - rader som börjar med # eller // (kommentarer)
      - kommandon innan en giltig PLACE skett
      - okända kommandon
    """
    world = World(5)# 5x5 värld
    robot = Robot(world)
    out = []

    for raw in lines:
        line = raw.strip()

        # Kommentarer och tomma rader
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        upper = line.upper()

        # PLACE hanteras separat
        if upper.startswith("PLACE"):
            args = read_place_string(line)
            if args:
                x, y, facing = args
                robot.place(x, y, facing)  # ogiltig place ignoreras av Robot
            # oavsett om det lyckades eller ej, gå vidare till nästa rad
            continue

        # Innan giltig PLACE: ignorera allt
        if not robot.state:
            continue

        if upper == "MOVE":
            robot.move()
        elif upper == "LEFT":
            robot.left()
        elif upper == "RIGHT":
            robot.right()
        elif upper == "REPORT":
            s = robot.report()
            if s is not None:
                out.append(s)
        else:
            
            continue

    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("Du behöver ange en fil med kommandon.")
        return 0  

    path = sys.argv[1]

    try:
        with open(path, "r", encoding="utf-8") as f:
            outputs = run_instructions(f.readlines())
    except OSError as e:
        
        print(f"Kunde inte läsa filen: {e}", file=sys.stderr)
        return 1

    
    for line in outputs:
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
