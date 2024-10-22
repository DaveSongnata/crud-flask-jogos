from crud import app, db
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos
from helpers import recoverimg, deleta_arquivo, FormularioJogo
import time


@app.route('/')
def index():
    if 'user_log' not in session or session['user_log'] ==  None:
        return redirect(url_for('login'))
    else: 
        ListaJogos = Jogos.query.order_by(Jogos.id)
        return render_template('index.html',  titulo='Jogos', jogos=ListaJogos)





#página     
@app.route('/novo')                      
def novo():
    if 'user_log' not in session or session['user_log'] ==  None:
       return redirect(url_for('login', proxima=url_for('novo')))
    else:
        form = FormularioJogo()
        return render_template ('novo.html', titulo='Cadastro', form=form)

#rota
@app.route('/criar', methods=['POST', ])                      
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria= form.categoria.data
    console= form.console.data

    jogo_duplicado = Jogos.query.filter_by(nome=nome).first()

    if jogo_duplicado:
         flash("Jogo já existente")
         return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa_{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))



@app.route('/editar/<int:id>')                      
def editar(id):
    if 'user_log' not in session or session['user_log'] ==  None:
       return redirect(url_for('login', proxima=url_for('editar')))
    else:
        jogo = Jogos.query.filter_by(id=id).first()
        form = FormularioJogo()
        form.nome.data = jogo.nome
        form.categoria.data = jogo.categoria
        form.console.data = jogo.console
        capa_jogo = recoverimg(id)
        return render_template ('editar.html', titulo='Editando Jogo', id=id, capa_jogo = capa_jogo, form=form)
    
    


@app.route('/atualizar', methods=['POST', ])                      
def atualizar():

    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id= request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.categoria.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)

        arquivo.save(f'{upload_path}/capa_{jogo.id}-{timestamp}.jpg')


    return redirect (url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'user_log' not in session or session['user_log'] ==  None:
       return redirect(url_for('login'))
    else:
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        deleta_arquivo(id)
        flash("Item deletado com Sucesso")
    return redirect(url_for('index'))



@app.route('/img/<nome_arquivo>')
def img(nome_arquivo): 
    return send_from_directory('uploads', nome_arquivo)
