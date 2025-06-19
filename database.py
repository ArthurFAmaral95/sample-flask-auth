#arquivo criado para import o sqlalchemy e iniciar o banco de dados
#se essa importacao fica no arquivo app.py vamos ter erro de referencia circular
#depois vamos importar no arquivo app.py a variavel db
from flask_sqlalchemy import SQLAlchemy

#iniciamos a instancia do SQLAlchemy
db = SQLAlchemy()


'''
CRIANDO O BANCO DE DADOS

para iniciar o banco de dados, vamos no terminal e damos o comando flask shell
depois db.create_all() para iniciar uma session e criar tudo que fizemos --> toda vez que conectamos em um db para fazer alguma operacao, abrimos uma session e quando terminamos temos que fecha-la. cada db tem um limite de quantas sessions abertas ele suporta simultaneamente
depois de criar usamos o db.session.commit() para mandar para o db o que foi feito na session
ao terminar usamos o comando exit() para sair do flask shell e finalizar a session
ao finalizar todo esse processo, uma pasta instance sera criada com o arquivo do banco de dados dentro
'''

''''
ADICIONANDO REGISTROS NO BANCO DE DADOS
abrir o terminal e iniciar o flask shell
criar uma instancia da classe User --> user = User(username='username', password='password')
adicionar a instancia --> db.session.add(user)
fazer o commit para o banco --> db.session.commit()
encerrar a sessao --> exit()
'''