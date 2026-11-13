import os
import unittest
from database import init_db, upsert_user, get_user, update_user_language, update_user_settings
from services.file_generator import create_temp_file

class TestSonicBot(unittest.TestCase):
    def setUp(self):
        # Use a test database
        os.environ['DB_PATH'] = 'test_sonic.db'
        init_db()

    def tearDown(self):
        if os.path.exists('test_sonic.db'):
            os.remove('test_sonic.db')

    def test_user_database_flow(self):
        # Test upsert
        upsert_user(12345, 'sonictest', 'Sonic User')
        user = get_user(12345)
        self.assertIsNotNone(user)
        self.assertEqual(user['first_name'], 'Sonic User')
        self.assertEqual(user['language'], 'en')
        self.assertEqual(user['settings'], 'balanced')

        # Test language update
        update_user_language(12345, 'ru')
        user = get_user(12345)
        self.assertEqual(user['language'], 'ru')

        # Test settings update
        update_user_settings(12345, 'creative')
        user = get_user(12345)
        self.assertEqual(user['settings'], 'creative')

    def test_file_generator(self):
        content = "print('Hello Sonic')"
        path = create_temp_file("test.py", content)
        self.assertTrue(os.path.exists(path))
        with open(path, 'r', encoding='utf-8') as f:
            read_content = f.read()
        self.assertEqual(read_content, content)
        os.remove(path)

if __name__ == '__main__':
    unittest.main()
