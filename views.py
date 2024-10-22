from crud import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
        form = FormularioUsuario()
        proxima = request.args.get('proxima', url_for('index'))        
        return render_template('login.html', proxima = proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario()
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
            session['user_log'] = usuario.nickname
            proxima_pagina = request.form.get('proxima', url_for('index'))
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou Senha Incorretos')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
     session ['user_log'] = None
     return redirect(url_for('login'))