from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime
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
                conn.execute("SELECT * FROM vagas WHERE  status_vaga = 'ATIVO'")

                resultado_vagas = conn.fetchall()
                contador = 1

                for vaga in resultado_vagas:
                    conn.execute(f"SELECT nome_empresa FROM empresa WHERE id_empresa = {vaga[1]};")

                    nome_empresa = conn.fetchone()

                    info_vagas = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">
                    {vaga[2]}
                    <div id = "div_id{contador}">
                    <ul>
                    <li><br>ID: {vaga[0]}<br>VAGA: {vaga[2]}<br>EMPRESA: {nome_empresa[0]}<br>FUNÇÃO: {vaga[3]}<br>SALÁRIO: R$ {vaga[4]:.2F}<br>STATUS: {vaga[5]}
                    </li>
                    <ul class="forms">
                    <li>
                    <form action="{ url_for('delete_vaga', vaga_id = vaga[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{ url_for('delete_vaga', vaga_id = vaga[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul>
                    </ul>
                    </div>
                    </li>'''
                    vagas.append(info_vagas)
                    contador += 1

                #ver empresas
                conn.execute("SELECT * FROM empresa  WHERE status_empresa = 'ATIVO'")

                resultado_empresas = conn.fetchall()
                

                for empresa in resultado_empresas:
                    info_empresas = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">{empresa[1]}<div id = "div_id{contador}"><ul><li><br>ID: {empresa[0]}<br>CNPJ: {empresa[2]}<br>LOCALIZAÇÃO: {empresa[3]}<br>PORTE: {empresa[4]}<br>DESCRIÇÃO: {empresa[5]}<br>STATUS: {empresa[6]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form action="{ url_for('delete_vaga', vaga_id = vaga[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{ url_for('delete_empresa', empresa_id = empresa[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div></li>'''  # Ajuste o índice conforme necessário
                    empresas.append(info_empresas)
                    contador += 1


                
                #ver candidatos
                conn.execute("SELECT * FROM candidato")
                resultado_candidato = conn.fetchall()
                

                for candidato in resultado_candidato:
                    info_candidato = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">{candidato[1]}<div id = "div_id{contador}"><ul><li><br>ID: {candidato[0]}<br>CPF: {candidato[2]}<br>TELEFONE: {candidato[3]}<br>ENDEREÇO: {candidato[4]}<br>E-MAIL: {candidato[5]}<br>STATUS: {candidato[6]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form action="{ url_for('delete_candidato', candidato_id = candidato[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{ url_for('delete_candidato', candidato_id = candidato[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div></li>'''  # Ajuste o índice conforme necessário
                    candidatos.append(info_candidato)
                    contador += 1



                #ver aplicações
                conn.execute("SELECT * FROM aplicacao WHERE status_aplicacao = 'ATIVO'")
                resultado_aplicacao = conn.fetchall()

                for aplicacao in resultado_aplicacao:
                    conn.execute(f"SELECT nome_vaga FROM portaldeempregos.vagas WHERE id_vaga = {aplicacao[2]};")
                    nome_vaga = conn.fetchone()

                    conn.execute(f"SELECT nome_candidato FROM portaldeempregos.candidato WHERE id_candidato = {aplicacao[1]}")
                    nome_candidato = conn.fetchone()


                    info_aplicacao = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">VAGA: {nome_vaga[0]}: CANDIDATO: {nome_candidato[0]}<div id = "div_id{contador}"><ul><li><br>ID: {aplicacao[0]}<br>ID CANDIDATO: {aplicacao[1]}<br>ID VAGA: {aplicacao[2]}<br>DATA APLICAÇÃO: {aplicacao[3]}<br>STATUS: {aplicacao[4]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form action="{ url_for('delete_aplicacao', aplicacao_id = aplicacao[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{ url_for('delete_aplicacao', aplicacao_id = aplicacao[0]) }" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div> </li>'''  # Ajuste o índice conforme necessário
                    aplicacoes.append(info_aplicacao)
                    contador += 1


    
    except Error as erro:
        logging.error(f'Erro ao buscar vagas: {erro}')
        vagas = ['Erro ao buscar vagas.']
        empresas = ['Erro ao buscar empresas.']
        candidato = ['Erro ao buscar candidatos.']
        aplicacoes = ['Erro ao buscar aplicações.']



    
    return render_template('index.html', username=session.get('username'), vagas_ver=vagas,  empresas_ver=empresas,  candidato_ver=candidatos, aplicacao_ver=aplicacoes)





@app.route('/delete_vaga/<int:vaga_id>', methods=['POST'])
def delete_vaga(vaga_id):
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos',
            auth_plugin='mysql_native_password'
        ) as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE aplicacao SET status_aplicacao = 'INATIVO' WHERE id_vaga = %s", (vaga_id,))
                conn.execute("UPDATE vagas SET status_vaga = 'INATIVO' WHERE id_vaga = %s", (vaga_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar vaga: {e}')
    return redirect(url_for('homepage'))

@app.route('/delete_empresa/<int:empresa_id>', methods=['POST'])
def delete_empresa(empresa_id):
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos',
            auth_plugin='mysql_native_password'
        ) as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE vagas SET status_vaga = 'INATIVO' WHERE id_empresa = %s", (empresa_id,))
                conn.execute("UPDATE empresa SET status_empresa = 'INATIVO' WHERE id_empresa = %s", (empresa_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar empresa: {e}')
    return redirect(url_for('homepage'))




@app.route('/delete_candidato/<int:candidato_id>', methods=['POST'])
def delete_candidato(candidato_id):
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos',
            auth_plugin='mysql_native_password'
        ) as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE vagas SET status_vaga = 'INATIVO' WHERE id_candidato = %s", (candidato_id,))
                conn.execute("UPDATE candidato SET status_candidato = 'INATIVO' WHERE id_candidato = %s", (candidato_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar candidato: {e}')
    return redirect(url_for('homepage'))





@app.route('/delete_aplicacao/<int:aplicacao_id>', methods=['POST'])
def delete_aplicacao(aplicacao_id):
    try:
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='portaldeempregos',
            auth_plugin='mysql_native_password'
        ) as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE vagas SET status_vaga = 'INATIVO' WHERE id_aplicacao = %s", (aplicacao_id,))
                conn.execute("UPDATE aplicacao SET status_aplicacao = 'INATIVO' WHERE id_aplicacao = %s", (aplicacao_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar aplicacao: {e}')
    return redirect(url_for('homepage'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
