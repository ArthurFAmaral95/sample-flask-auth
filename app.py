from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager #gerencia o login dos usuarios
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #caminho do banco de dados

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

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
      return jsonify({'message':'Autenticação realizada com sucesso'})

  return jsonify({'message':'Credencias inválidas'}), 400

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'hello world'


if __name__ == '__main__':
  app.run(debug=True)