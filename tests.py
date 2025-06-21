import pytest
import requests
import uuid

BASE_URL = 'http://127.0.0.1:5000'
users = []

new_user_data = {
   'username': f'test_{uuid.uuid4().hex[:8]}',
   'password': '1234'
 }

user_data_erro = {
   'username': 'test_erro'
 }

def test_create_user():
  global new_user_data
  response = requests.post(f'{BASE_URL}/user',json=new_user_data)
  assert response.status_code == 200
  response_json = response.json()
  assert 'message' in response_json
  assert 'user_id' in response_json
  users.append(response_json['user_id'])

  global user_data_erro
  response = requests.post(f'{BASE_URL}/user', json=user_data_erro)
  assert response.status_code == 400
  response_json = response.json()
  assert 'message' in response_json

def test_login():
  global new_user_data
  response = requests.post(f'{BASE_URL}/login', json=new_user_data)
  assert response.status_code == 200
  response_json = response.json()
  assert 'message' in response_json

  global user_data_erro
  response = requests.post(f'{BASE_URL}/user', json=user_data_erro)
  assert response.status_code == 400
  response_json = response.json()
  assert 'message' in response_json

def test_read_user():
  user = users[0]
  response = requests.get(f'{BASE_URL}/user/{user}')
  assert response.status_code == 200
  response_json = response.json()
  assert 'username' in response_json

  response = requests.get(f'{BASE_URL}/user/99999')
  assert response.status_code == 404
  response_json = response.json()
  assert 'message' in response_json

def test_logout():
  response = requests.get(f'{BASE_URL}/logout')
  assert response.status_code == 200
  response_json = response.json()
  assert 'message' in response_json