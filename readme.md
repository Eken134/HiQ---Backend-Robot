Robot Simulator (HIQ)

Ett Python-projekt som simulerar en robot som rör sig på ett 5×5-bord.  

---

Koordinatsystem och riktningar:

Utgår från ett klassiskt kartesiskt plan där (0, 0) ligger i nedre vänstra hörnet.

y ↑
4 |     NORTH ↑
3 |
2 |
1 |
0 |----------------→
    0 1 2 3 4



Riktningarna hanteras i ordningen:

DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]

Rotationer fungerar som en cirkulär lista:

RIGHT → +1 steg i listan
LEFT → −1 steg

Varje riktning har en rörelsevektor (dx, dy):
Direction	dx	dy	Effekt
NORTH	0	+1	Gå uppåt på y-axeln
EAST	+1	0	Gå åt höger på x-axeln
SOUTH	0	−1	Gå nedåt på y-axeln
WEST	−1	0	Gå åt vänster på x-axeln


Filer:
robot.py	Kärnlogiken: World, State, Robot
simulator.py	Körbar tolk som läser kommandon från fil
test/test_robot.py	Enhetstester för värld och robot
test/test_simulator.py	End-to-end-tester med hela kommandosekvenser

För att köra en färdig testsats (t.ex. a.txt):
python simulator.py testdata/a.txt


Tester körs enklast via:
python -m unittest discover -s test -p "test*.py" -v


Vad som testas:

robot.py:
Att världen (World) korrekt avgör om en punkt ligger inom 5×5-gränsen.
Att State roterar och flyttar korrekt beroende på riktning.
Att rörelse blockeras vid bordskanten.
Att Robot ignorerar kommandon innan PLACE, ignorerar ogiltiga PLACE, och ersätter tidigare placering.

simulator.py:
Att parsern (read_place_string) klarar whitespace, små/bokstäver och kommatecken.
Att roboten producerar rätt output för exemplen a/b/c.
Att kommandon innan PLACE ignoreras.
Att rörelser vid kanterna blockeras.
Att ogiltiga PLACE ignoreras men giltiga senare accepteras.
