import pytest
import requests
from models.user import User
from flask_login import FlaskLoginClient
from app import app, db
import bcrypt
import uuid

new_user_data = {
   'username': f'login_generatd_test_{uuid.uuid4().hex[:8]}',
   'password': '1234'
 }

user_data_erro = {
   'username': 'test_erro'
 }

app.test_client_class = FlaskLoginClient
app.testing = True

@pytest.fixture
def client():
  return app.test_client()

@pytest.fixture
def user():
  with app.app_context():
    username = f'fixture_generated_test_{uuid.uuid4().hex[:8]}'
    password = bcrypt.hashpw(str.encode('1234'), bcrypt.gensalt())
    user = User(username=username, password=password, role='user')
    db.session.add(user)
    db.session.commit()
    return user

BASE_URL = 'http://127.0.0.1:5000'

def test_create_user(client):
  global new_user_data
  response = client.post('/user',json=new_user_data)
  assert response.status_code == 200
  response_json = response.get_json()
  assert 'message' in response_json
  assert 'user_id' in response_json

  global user_data_erro
  response = client.post('/user', json=user_data_erro)
  assert response.status_code == 400
  response_json = response.get_json()
  assert 'message' in response_json

def test_login(client):
  global new_user_data
  response = client.post('/login', json=new_user_data)
  assert response.status_code == 200
  response_json = response.get_json()
  assert 'message' in response_json

  global user_data_erro
  response = client.post('/login', json=user_data_erro)
  assert response.status_code == 400
  response_json = response.get_json()
  assert 'message' in response_json

def test_read_user(client, user):
  with client.login(user):
    response = client.get(f'/user/{user.id}')
    assert response.status_code == 200
    response_json = response.get_json()
    assert 'username' in response_json
    assert response_json['username'] == user.username

  with client.login(user):
    response = client.get(f'/user/99999')
    assert response.status_code == 404
    response_json = response.get_json()
    assert 'message' in response_json

# def test_update_user():
#   user = users[0]
#   new_test_password = {
#     'password':'1234'
#   }
#   response = requests.put(f'{BASE_URL}/user/{user}', json=new_test_password)
#   assert response.status_code == 200
#   response_json = response.json()
#   assert 'message' in response_json

# def test_logout():
#   response = requests.get(f'{BASE_URL}/logout')
#   assert response.status_code == 200
#   response_json = response.json()
#   assert 'message' in response_json