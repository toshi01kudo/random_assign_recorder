import unittest
import shutil
import sys
sys.path.append('..')
import random_assign


class TestAssign(unittest.TestCase):
    def test_random_assign(self):
        shutil.copyfile("../.env.example", "../.env")
        random_assign.main()
        with open('../assigned.txt', 'r', encoding="utf-8") as f:
            done_pool = f.read().split(',')
        self.assertAlmostEqual(len(done_pool), 1)


if __name__ == "__main__":
    unittest.main()
