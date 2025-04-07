import unittest
from src.geometry.primitives import Line

class TestPrimitives(unittest.TestCase):
    def test_line_vertices(self):
        line = Line((0, 0, 0), (1, 1, 1))
        self.assertEqual(line.get_vertices(), [(0, 0, 0), (1, 1, 1)])

if __name__ == '__main__':
    unittest.main()