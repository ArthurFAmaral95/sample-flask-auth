from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user #gerencia o login dos usuarios
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

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'hello world'


if __name__ == '__main__':
  app.run(debug=True)