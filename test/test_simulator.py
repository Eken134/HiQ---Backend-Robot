# test/test_simulator.py
"""
Lista:
- Parser: read_place_string tolkar PLACE robust.
- run_instructions: kör exemplen a/b/c.
- run_instructions: ignorerar före PLACE, blockerar vid kant,
  ignorerar ogiltiga PLACE.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from simulator import run_instructions, read_place_string


class TestParser(unittest.TestCase):
    """PLACE-rader till (x,y,facing)."""
    def test_read_place_string(self):
        self.assertEqual(read_place_string("PLACE,1,2,NORTH"), (1, 2, "NORTH"))
        self.assertEqual(read_place_string("PLACE 1,2,west"), (1, 2, "WEST"))
        self.assertIsNone(read_place_string("PLACE,1,NORTH"))
        self.assertIsNone(read_place_string("MOVE"))


class TestRunHappyPath(unittest.TestCase):
    """Exempel från uppgiften."""
    def test_example_a(self):
        self.assertEqual(
            run_instructions(["PLACE,0,0,NORTH", "MOVE", "REPORT"]),
            ["0,1,NORTH"],
        )

    def test_example_b(self):
        self.assertEqual(
            run_instructions(["PLACE,0,0,NORTH", "LEFT", "REPORT"]),
            ["0,0,WEST"],
        )

    def test_example_c(self):
        self.assertEqual(
            run_instructions(["PLACE,1,2,EAST", "MOVE", "MOVE", "LEFT", "MOVE", "REPORT"]),
            ["3,3,NORTH"],
        )


class TestRunEdgesAndInvalid(unittest.TestCase):
    """Kanter, ogiltiga kommandon, ordning."""
    def test_ignore_until_place(self):
        self.assertEqual(
            run_instructions(["MOVE", "LEFT", "REPORT", "PLACE,0,0,NORTH", "REPORT"]),
            ["0,0,NORTH"],
        )

    def test_block_at_edges(self):
        self.assertEqual(
            run_instructions(["PLACE,0,4,NORTH", "MOVE", "REPORT", "RIGHT", "MOVE", "REPORT"]),
            ["0,4,NORTH", "1,4,EAST"],
        )

    def test_invalid_place_then_valid(self):
        self.assertEqual(
            run_instructions(["PLACE,9,9,NORTH", "MOVE", "PLACE,2,2,SOUTH", "REPORT"]),
            ["2,2,SOUTH"],
        )


if __name__ == "__main__":
    unittest.main()
