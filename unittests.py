import unittest
from src.app import app, db
from src.app.models import User, Beat, Comment, Like
from io import BytesIO
import bcrypt

class YourAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client(use_cookies=True)

        hashed_password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
        user = User(email='test@example.com', id='testuser', passwd=hashed_password)
        beat = Beat(id='testbeat', title='Test Beat', artist=user.id)
        db.session.add_all([user, beat])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, user_id, password):
        return self.client.post('/home', data=dict(
            id=user_id,
            passwd=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/users/signout', follow_redirects=True)

    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        response = self.client.post('/users/signup', data=dict(
            email_address='newuser@example.com',
            id='newuser',
            passwd='newpassword',
            passwd_confirm='newpassword'
        ), follow_redirects=True)
        self.assertIn(b'Account created successfully!', response.data)

    def test_user_login_logout(self):
        response = self.login('testuser', 'password')
        # Add an assertion here to check for successful login if your application provides any indication
        self.assertEqual(response.status_code, 200)  # Assuming successful login redirects or responds with 200
        response = self.logout()
        # Add an assertion here to check for successful logout if your application provides any indication
        self.assertEqual(response.status_code, 200)  # Assuming successful logout redirects or responds with 200

    def test_beat_creation(self):
        self.login('testuser', 'password')
        data = {
            'title': 'New Beat',
            'genre': 'jazz',
            'description': 'Test description',
            'audio_file': (BytesIO(b'my file contents'), 'test.mp3')
        }
        response = self.client.post('/beats/new', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertIn(b'Beat created successfully!', response.data)

    def test_add_comment(self):
        # Ensure user is logged in
        self.login('testuser', 'password')

        # Check if a beat with the given ID exists, create if not
        beat = Beat.query.get('unique_testbeat')
        if not beat:
            beat = Beat(id='unique_testbeat', title='Test Beat', artist='testuser', audio_file='test.mp3')
            db.session.add(beat)
            db.session.commit()

        # Make a POST request to add a comment
        response = self.client.post('/add-comment/unique_testbeat', data=dict(content='Great beat!'), follow_redirects=True)

        # Check if the response contains the expected message
        self.assertIn(b'Your comment has been added.', response.data)
        self.assertEqual(response.status_code, 200)  # Additionally, check if the response status is 200

    def test_like_song(self):
        self.login('testuser', 'password')
        response = self.client.post('/like/testbeat', follow_redirects=True)
        # Adjust the assertion according to the actual JSON response
        self.assertIn(b'success', response.data)

    def test_delete_beat(self):
        self.login('testuser', 'password')
        response = self.client.post('/beat_user/testuser/delete/testbeat', follow_redirects=True)
        self.assertIn(b'Beat deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
