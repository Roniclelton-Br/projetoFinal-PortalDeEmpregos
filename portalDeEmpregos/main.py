from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import logging

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    texto = ''
    if request.method == 'POST':
        try:
            conexao_bd = pymysql.connect(
                host='localhost',
                user='root',
                password='mysql',
                database='portaldeempregos'
            )
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
        except pymysql.MySQLError as e:
            logging.error(f'Erro ao conectar ao banco de dados: {e}')
            texto = 'Erro ao conectar ao banco de dados.'
        finally:
            if conexao_bd:
                conexao_bd.close()
    return render_template('login.html', texto=texto)

@app.route('/index')
def homepage():
    vagas = []
    empresas = []

    try:
        conexao_bd = pymysql.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos'
        )
        with conexao_bd.cursor() as conn:
            # Ver vagas
            conn.execute("SELECT * FROM vagas")
            resultado_vagas = conn.fetchall()

            for vaga in resultado_vagas:
                info_vagas = f'<li class="ver">{vaga[2]}</li>'
                vagas.append(info_vagas)
              
            # Ver empresas
            conn.execute("SELECT * FROM empresa")
            resultado_empresas = conn.fetchall()

            for empresa in resultado_empresas:
                info_empresas = f'<li class="ver">{empresa[1]}</li>'
                empresas.append(info_empresas)
    except pymysql.MySQLError as erro:
        logging.error(f'Erro ao buscar dados: {erro}')
        vagas = ['Erro ao buscar vagas.']
        empresas = ['Erro ao buscar empresas.']
    finally:
        if conexao_bd:
            conexao_bd.close()

    return render_template('index.html', username=session.get('username'), vagas_ver=vagas, empresas_ver=empresas)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
