from flask import request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models.user import User
from database import db
import bcrypt

def register_routes(app):
  #rota para o usuario fazer o login
  @app.route('/login', methods=['POST'])
  def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #login só vair ser feito se na request tiver username e password. se alguma dessas informações estiver faltando vamos retornar para o usuario uma mensagem de erro
    if username and password:
      user = User.query.filter_by(username=username).first() #o metodo filter_by retorna uma lista, por isso temos que usar o first para retornar somente o primeiro valor encontrado
      if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
        login_user(user) #faz o login e a autenticacao do usuario
        print(current_user.is_authenticated)
        return jsonify({'message':'Autenticação realizada com sucesso'})

    return jsonify({'message':'Credencias inválidas'}), 400

  @app.route('/logout', methods=['GET'])
  # @login_required #decorator que vai proteger essa rota --> só vai ser executada se o usuario estiver logado --> se tentarmos fazer o logout sem estar logado vamos ter uma mensagem de erro
  def logout():
    logout_user()
    return jsonify({'message':'Logout realizado com sucesso.'})

  @app.route('/user', methods=['POST'])
  def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
      hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
      user = User(username=username, password=hashed_password, role='user')
      db.session.add(user)
      db.session.commit()
      return jsonify({'message':'Usuario cadastrado com sucesso.', 'user_id':user.id})

    return jsonify({'message':'Dados inválidas.'}), 400

  @app.route('/user/<int:user_id>', methods=['GET'])
  # @login_required
  def read_user(user_id):
    user = User.query.get(user_id)

    if user:
      return jsonify({'username':user.username})
  
    return jsonify({'message': 'Usuario não encontrado'}), 404

  @app.route('/user/<int:user_id>', methods=['PUT'])
  # @login_required
  def update_user(user_id):
    user = User.query.get(user_id)
    data = request.json

    if user_id != current_user.id and current_user.role == 'user':
      return jsonify({'message':'Operação não permitida'}),403
    elif user and data.get('password'):
      password = data.get('password')
      hashed_password = bcrypt.hashpw(str.encode(password),bcrypt.gensalt())
      user.password = hashed_password
      db.session.commit()
      return jsonify({'message':f'Usuario {user_id} atualizado com sucesso'})
  
    return jsonify({'message':'Usuario não encontrado'}),400

  @app.route('/user/<int:user_id>', methods=['DELETE'])
  # @login_required
  def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role != 'admin':
      return jsonify({'message': 'Operação não permitida'}), 403
    elif user_id == current_user.id:
      return jsonify({'message': 'Deleção não permitida,'}), 403
    elif user:
      db.session.delete(user)
      db.session.commit()
      return jsonify({'message':f'Usuario {user_id} deletado com sucesso'})
  
    return jsonify({'message':'Usuario não encontrado'}), 400
