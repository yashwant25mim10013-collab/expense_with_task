import unittest
from utils.validators import required

class TestTasks(unittest.TestCase):
    def test_required(self):
        self.assertTrue(required("Task"))
        self.assertFalse(required(""))

if __name__ == "__main__":
    unittest.main()
