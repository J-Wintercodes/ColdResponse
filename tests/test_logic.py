import unittest
from logic import calculate_auto_rating
from database import get_connection, create_tables

class TestLogic(unittest.TestCase):

    def setUp(self):
        # Temporäre DB für Tests
        self.conn = get_connection()
        create_tables()

    def tearDown(self):
        self.conn.close()

    def test_auto_rating_basic(self):
        email = {"subject": "urgent meeting", "body": "please respond", "message_id": "1"}
        rating = calculate_auto_rating(email)
        self.assertGreater(rating, 0)

if __name__ == "__main__":
    unittest.main()
