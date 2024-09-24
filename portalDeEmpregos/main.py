from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/', methods=['GET','POST'])
def login():
    texto = ''  # Inicializando a variável de texto
    if request.method == 'POST':
        try:
            conexao_bd = mysql.connector.connect(
                host='localhost',
                user='root',
                password='mysql',
                database='portaldeempregos',
                auth_plugin='mysql_native_password'
            )
            with conexao_bd.cursor() as conn:
                username = request.form['username']
                password = request.form['password']

                conn.execute('SELECT * FROM adm WHERE username_adm = %s', (username,))
                usuario = conn.fetchone()  # Use fetchone para pegar um único usuário

                if usuario:
                    if usuario[-1] == password:  # Altere o índice se necessário
                        print(usuario)
                        session['username'] = usuario[1]
                        return redirect(url_for('homepage'))
                    else:
                        texto = 'Senha incorreta'
                else:
                    texto = 'Usuário incorreto'
        except Error as e:
            texto = f'Erro de conexão: {e}'
        finally:
            if conexao_bd.is_connected():
                conexao_bd.close()  # Feche a conexão após o uso

    return render_template('login.html', texto=texto)

@app.route('/index')
def homepage():
    return render_template('index.html',  username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)
