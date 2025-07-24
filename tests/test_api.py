import pytest
import json
import sys
import os
from init_db import init_db


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data

def test_not_found(client):
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_user_success(client):
    response = client.get('/user/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "password" not in data  # Password should not be returned

def test_get_user_not_found(client):
    response = client.get('/user/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

# User creation tests
def test_create_user_success(client):
    response = client.post('/users',
                          json={"name": "Test User", "email": "test@example.com", "password": "testpass123"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "message" in data
    assert "user_id" in data

def test_create_user_invalid_input(client):
    response = client.post('/users',
                          json={"name": "Test User"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "errors" in data

def test_create_user_invalid_email(client):
    response = client.post('/users',
                          json={"name": "Test User", "email": "invalid-email", "password": "testpass123"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "errors" in data

# User update tests
def test_update_user_success(client):
    response = client.put('/user/1',
                         json={"name": "Updated Name", "email": "updated@example.com"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "user" in data
    assert data["user"]["name"] == "Updated Name"
    assert data["user"]["email"] == "updated@example.com"

def test_update_user_not_found(client):
    response = client.put('/user/999',
                         json={"name": "Updated Name", "email": "updated@example.com"})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

def test_update_user_invalid_input(client):
    response = client.put('/user/1',
                         json={"name": ""})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "errors" in data

# User deletion tests
def test_delete_user_success(client):
    get_response = client.get('/user/2')
    if get_response.status_code == 200:
        # Then delete the user
        response = client.delete('/user/2')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
        # Verify the user is deleted
        verify_response = client.get('/user/2')
        assert verify_response.status_code == 404

def test_delete_user_not_found(client):
    response = client.delete('/user/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

# Search tests
def test_search_users_success(client):
    response = client.get('/search?name=John')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_search_users_no_name(client):
    response = client.get('/search')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


@pytest.fixture
def login_db_setup():
    """Setup database specifically for login tests"""
    # Delete the database if it exists
    if os.path.exists('users.db'):
        os.remove('users.db')

    
    init_db()
    
    yield


def test_login_success(client, login_db_setup):
    # This test assumes the database has been initialized with sample data
    response = client.post('/login', 
                          json={"email": "john@example.com", "password": "password123"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"

def test_login_failure(client):
    response = client.post('/login', 
                          json={"email": "john@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["status"] == "failed"

def test_login_invalid_input(client):
    response = client.post('/login', 
                          json={"email": "john@example.com"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "errors" in data