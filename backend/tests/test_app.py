import unittest
from werkzeug.security import generate_password_hash
from backend.app import app, db  # Adjust these imports to your project structure
from backend.models import User

class BlackjackTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app to use the testing configuration
        app.config.from_object('backend.app.TestConfig')

        # Set up the Flask test client
        self.app = app.test_client()

        # Set up the application context and create the test database
        with app.app_context():
            db.create_all()
            self.create_test_user()

    def create_test_user(self):
        # Check if user exists, if not, create a test user
        if not User.query.filter_by(username='test').first():
            user = User(username='test', password_hash=generate_password_hash('test'))
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        # Tear down and clean up the test database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Your test methods
    def test_new_game(self):
        # Example test for the new_game endpoint
        response = self.app.get('/new_game')  # Adjust the endpoint as necessary
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Example test for the login endpoint
        response = self.app.post('/auth/login', json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
