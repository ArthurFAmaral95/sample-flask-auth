from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'your_secret_key'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud' #caminho do banco de dados

  
  db.init_app(app)
  login_manager.init_app(app)

  #login --> definie qual a rota o app deve usar como rota de login
  login_manager.login_view = 'login'

  #funcao necessaria para carregar o usuario e possibilitar que o flask verifique o usuario no banco todas as vezes que necessario
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(user_id)
  
  from routes import register_routes
  register_routes(app)

  return app
  
if __name__ == '__main__':
  create_app().run(debug=True)