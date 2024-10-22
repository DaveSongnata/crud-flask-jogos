import os

SECRET_KEY = 'colloportus'

#CONFIGURA O BANCO MYSQL PARA RODAR 
SQLALCHEMY_DATABASE_URI = \
'{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'brasteroot',
    servidor = 'localhost',
    database = 'jogoteca'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'