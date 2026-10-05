import unittest
from database.database import init_db

class TestDatabase(unittest.TestCase):
    def test_database_init(self):
        init_db()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
