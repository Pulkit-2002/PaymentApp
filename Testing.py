# calculator.py

def add_numbers(a, b):
    return a + b

# test_calculator.py
from calculator import add_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    # Add more test cases as needed
pytest test_calculator.py

# test_app.py
from app import app, db

class TestApp:
    def setup_method(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        assert b'Welcome to My App' in response.data

    # Add more integration tests as needed
pytest test_app.py




