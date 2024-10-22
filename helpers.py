import os
from crud import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.length(min=1, max=50)])
    categoria = StringField('Categoria do Jogo', [validators.DataRequired(), validators.length(min=1, max=40)])
    console = StringField('Console do Jogo', [validators.DataRequired(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar') 

class FormularioUsuario(FlaskForm):
    nickname = StringField('Usuário', [validators.DataRequired(), validators.length(min=1, max=50)])
    senha = PasswordField('Senha',[validators.DataRequired(), validators.length(min=1, max=100)])
    login = SubmitField('Login')


def recoverimg(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo

    return 'default.jpg'

def deleta_arquivo(id):
    arquivo = recoverimg(id)
    if arquivo != 'default.jpg':
        print("newbas\n n \n n \n n \n n")
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
    else:
        print("something wrong... \n \n \n n \n n \n n ")