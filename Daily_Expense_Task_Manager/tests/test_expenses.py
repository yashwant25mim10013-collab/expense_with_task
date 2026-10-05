import unittest
from utils.validators import valid_amount

class TestExpenses(unittest.TestCase):
    def test_valid_amount(self):
        self.assertTrue(valid_amount("100"))
        self.assertFalse(valid_amount("-5"))

if __name__ == "__main__":
    unittest.main()
