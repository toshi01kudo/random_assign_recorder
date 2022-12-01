import unittest
import shutil
import sys
sys.path.append('..')
import random_assign


class TestAssign(unittest.TestCase):
    def test_random_assign(self):
        shutil.copyfile("../.env.example", "../.env")
        selected = random_assign.main(assign_num=2)
        self.assertAlmostEqual(len(selected), 2)


if __name__ == "__main__":
    unittest.main()
