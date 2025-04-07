import unittest
from src.transforms.transformations import translate

class TestTransformations(unittest.TestCase):
    def test_translate(self):
        point = (1, 2, 3)
        vector = (1, 1, 1)
        translated = translate(point, vector)
        self.assertEqual(translated, (2, 3, 4))

if __name__ == '__main__':
    unittest.main()