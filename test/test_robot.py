# test/test_robot.py
"""
Lista:
- World: in_bounds() identifierar punkter inne/ute.
- State: rotation, nästa koordinat, blockering vid kant.
- Robot: ignorerar allt innan PLACE, placerar sig korrekt,
         ignorerar ogiltig PLACE, ny PLACE ersätter gammal.
"""

import unittest
from robot import World, State, Robot


class TestWorld(unittest.TestCase):
    """Grundfall för världens gränslogik."""
    def test_in_bounds(self):
        w = World(5)
        self.assertTrue(w.in_bounds(0, 0))
        self.assertTrue(w.in_bounds(4, 4))
        self.assertFalse(w.in_bounds(-1, 0))
        self.assertFalse(w.in_bounds(0, 5))


class TestState(unittest.TestCase):
    """Rotation och förflyttning på state-nivå."""
    def test_rotation_left_right(self):
        s = State(0, 0, "NORTH")
        s.right(); self.assertEqual(s.facing, "EAST")
        s.right(); self.assertEqual(s.facing, "SOUTH")
        s.left();  self.assertEqual(s.facing, "EAST")
        s.left();  self.assertEqual(s.facing, "NORTH")

    def test_next_xy_by_facing(self):
        cases = [
            ("NORTH", (1, 1), (1, 2)),
            ("EAST",  (1, 1), (2, 1)),
            ("SOUTH", (1, 1), (1, 0)),
            ("WEST",  (1, 1), (0, 1)),
        ]
        for facing, start, expected in cases:
            with self.subTest(facing=facing):
                s = State(*start, facing)
                self.assertEqual(s.next_xy(), expected)

    def test_move_if_valid_blocks_at_edge(self):
        w = World(5)
        s = State(0, 4, "NORTH")
        self.assertFalse(s.move_if_valid(w))
        self.assertEqual((s.x, s.y), (0, 4))


class TestRobot(unittest.TestCase):
    """Robotens regler ovanpå World/State."""
    def test_ignores_until_place(self):
        r = Robot(World(5))
        r.move(); r.left(); r.right()
        self.assertIsNone(r.report())

    def test_place_move_report_happy_path(self):
        r = Robot(World(5))
        r.place(0, 0, "NORTH")
        r.move()
        self.assertEqual(r.report(), "0,1,NORTH")

    def test_place_outside_world_is_ignored(self):
        r = Robot(World(5))
        r.place(9, 9, "NORTH")
        self.assertIsNone(r.report())

    def test_place_can_replace_previous(self):
        r = Robot(World(5))
        r.place(0, 0, "NORTH")
        r.place(2, 3, "WEST")
        self.assertEqual(r.report(), "2,3,WEST")


if __name__ == "__main__":
    unittest.main()
