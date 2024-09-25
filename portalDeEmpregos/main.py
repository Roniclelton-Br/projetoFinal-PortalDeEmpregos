from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import logging

app = Flask(__name__)
app.secret_key = 'my_secret_key'

logging.basicConfig(level=logging.ERROR)  # Configuração de registro

@app.route('/', methods=['GET', 'POST'])
def login():
    texto = ''
    if request.method == 'POST':
        try:
            with mysql.connector.connect(
                host='localhost',
                user='root',
                password='mysql',
                database='portaldeempregos',
                auth_plugin='mysql_native_password'
            ) as conexao_bd:
                with conexao_bd.cursor() as conn:
                    username = request.form['username']
                    password = request.form['password']

                    conn.execute('SELECT * FROM adm WHERE username_adm = %s', (username,))
                    usuario = conn.fetchone()

                    if usuario:
                        if password == usuario[-1]:  # Comparando a senha em texto puro
                            session['username'] = usuario[1]
                            return redirect(url_for('homepage'))
                        else:
                            texto = 'Senha incorreta'
                    else:
                        texto = 'Usuário incorreto'
        except Error as e:
            logging.error(f'Erro de conexão: {e}')
            texto = 'Erro ao conectar ao banco de dados.'
    return render_template('login.html', texto=texto)

@app.route('/index')
def homepage():
    vagas = []  # Lista para armazenar as vagas
    empresas = []
    candidatos = []
    aplicacoes = []

    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos',
            auth_plugin='mysql_native_password'
        ) as conexao_bd:
            with conexao_bd.cursor() as conn:
                # Ver vagas
                conn.execute("SELECT * FROM vagas")
                resultado_vagas = conn.fetchall()

                for vaga in resultado_vagas:
                    info_vagas = f'<li class="ver">{vaga[2]}</li>'  # Ajuste o índice conforme necessário
                    vagas.append(info_vagas)
              
                #ver empresas
                conn.execute("SELECT * FROM empresa")
                resultado_empresas = conn.fetchall()

                for empresa in resultado_empresas:
                    info_empresas = f'<li class="ver">{empresa[1]}</li>'  # Ajuste o índice conforme necessário
                    empresas.append(info_empresas)


                
                #ver candidatos
                conn.execute("SELECT * FROM candidato")
                resultado_candidato = conn.fetchall()

                for candidato in resultado_candidato:
                    info_candidato = f'<li class="ver">{candidato[1]}<br><br>ID: {candidato[0]}<br>CPF: {candidato[2]}<br>TELEFONE: {candidato[3]}<br>ENDEREÇO: {candidato[4]}</li>'  # Ajuste o índice conforme necessário
                    candidatos.append(info_candidato)



                #ver aplicações
                conn.execute("SELECT * FROM aplicacao")
                resultado_aplicacao = conn.fetchall()

                for aplicacao in resultado_aplicacao:
                    info_aplicacao = f'<li class="ver">ID: {aplicacao[0]} </li>'  # Ajuste o índice conforme necessário
                    aplicacoes.append(info_aplicacao)


    
    except Error as erro:
        logging.error(f'Erro ao buscar vagas: {erro}')
        vagas = ['Erro ao buscar vagas.']
        empresas = ['Erro ao buscar empresas.']
        candidato = ['Erro ao buscar candidatos.']
        aplicacoes = ['Erro ao buscar aplicações.']



    
    return render_template('index.html', username=session.get('username'), vagas_ver=vagas,  empresas_ver=empresas,  candidato_ver=candidatos, aplicacao_ver=aplicacoes)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
