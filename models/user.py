from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  #id (int), username (str), password (str), role (str)
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True) #valor dentro do String(80) é a quantidade maxima de caracteres e nullable é a permissao se a coluna pode estar vazia ou nao
  password = db.Column(db.String(80), nullable=False)
  role = db.Column(db.String(80), nullable=False, default='user')
