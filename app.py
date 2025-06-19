from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required #gerencia o login dos usuarios
import os

caminho_arquivo = 'modulo_4/sample-flask-auth/instance/database.db'
caminho_absoluto = os.path.abspath(caminho_arquivo)
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{caminho_absoluto}' #caminho do banco de dados

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

#login --> definie qual a rota o app deve usar como rota de login
login_manager.login_view = 'login'

#funcao necessaria para carregar o usuario e possibilitar que o flask verifique o usuario no banco todas as vezes que necessario
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

#rota para o usuario fazer o login
@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  #login só vair ser feito se na request tiver username e password. se alguma dessas informações estiver faltando vamos retornar para o usuario uma mensagem de erro
  if username and password:
    user = User.query.filter_by(username=username).first() #o metodo filter_by retorna uma lista, por isso temos que usar o first para retornar somente o primeiro valor encontrado
    if user and user.password == password:
      login_user(user) #faz o login e a autenticacao do usuario
      print(current_user.is_authenticated)
      return jsonify({'message':'Autenticação realizada com sucesso'})

  return jsonify({'message':'Credencias inválidas'}), 400

@app.route('/logout', methods=['GET'])
@login_required #decorator que vai proteger essa rota --> só vai ser executada se o usuario estiver logado --> se tentarmos fazer o logout sem estar logado vamos ter uma mensagem de erro
def logout():
  logout_user()
  return jsonify({'message':'Logout realizado com sucesso.'})

@app.route('/user', methods=["POST"])
@login_required #só vamos conseguir registrar um novo usuario se estivermos logados em outro --> esse decorator pode proteger qualquer rota que precise de autenticacao para ser executda
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'Usuario cadastrado com sucesso.'})

  return jsonify({'message':'Dados inválidas.'}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
  user = User.query.get(user_id)

  if user:
    return jsonify({'username':user.username})
  
  return jsonify({'message': 'Usuario não encontrado'}), 404

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'hello world'


if __name__ == '__main__':
  app.run(debug=True)