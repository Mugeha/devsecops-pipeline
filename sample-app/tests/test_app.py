"""
Basic tests for the sample app
"""

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_user_endpoint(client):
    """Test user endpoint"""
    rv = client.get('/user/testuser')
    assert rv.status_code == 200

def test_search_endpoint(client):
    """Test search endpoint"""
    rv = client.get('/search?q=test')
    assert rv.status_code == 200
    assert b'test' in rv.data