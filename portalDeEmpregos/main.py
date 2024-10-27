from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2 import Error
import logging
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'my_secret_key')  # Usando variável de ambiente para a chave secreta

logging.basicConfig(level=logging.ERROR)

# Configuração do banco de dados PostgreSQL
db_config = {
    'host': os.getenv('DB_HOST', 'aimlessly-sincere-hermit.data-1.use1.tembo.io'),
    'port': os.getenv('DB_PORT', 5432),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'ad3rq0MRExKqHJTo'),
    'dbname': os.getenv('DB_NAME', 'portaldeempregos')
}

def get_db_connection():
    return psycopg2.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def login():
    texto = ''
    if request.method == 'POST':
        try:
            with get_db_connection() as conexao_bd:
                with conexao_bd.cursor() as conn:
                    username = request.form['username']
                    password = request.form['password']

                    conn.execute('SELECT * FROM adm WHERE username_adm = %s', (username,))
                    usuario = conn.fetchone()

                    if usuario:
                        if password == usuario[-1]:
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
    vagas, empresas, candidatos, aplicacoes = [], [], [], []

    try:
        with get_db_connection() as conexao_bd:
            with conexao_bd.cursor() as conn:
                # Ver vagas
                conn.execute("SELECT * FROM vagas WHERE status_vaga = 'ATIVO' ORDER BY nome_vaga ASC;")
                resultado_vagas = conn.fetchall()
                contador = 1

                for vaga in resultado_vagas:
                    conn.execute("SELECT nome_empresa FROM empresa WHERE id_empresa = %s;", (vaga[1],))
                    nome_empresa = conn.fetchone()
                    nome_empresa_text = nome_empresa[0] if nome_empresa else 'Desconhecida'

                    info_vagas = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">
                    {vaga[2]}
                    <div id="div_id{contador}">
                    <ul>
                    <li><br>ID: {vaga[0]}<br>VAGA: {vaga[2]}<br>EMPRESA: {nome_empresa_text}<br>FUNÇÃO: {vaga[3]}<br>SALÁRIO: R$ {vaga[4]:.2F}<br>STATUS: {vaga[5]}
                    </li>
                    <ul class="forms">
                    <li>
                    <form style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{url_for('delete_vaga', vaga_id=vaga[0])}" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    <li>
                    <form style="display:inline;">
                    <button type="submit">Aplicar para a vaga</button>
                    </form>
                    </li>
                    </ul>
                    </ul>
                    </div>
                    </li>'''
                    vagas.append(info_vagas)
                    contador += 1

                # Ver empresas
                conn.execute("SELECT * FROM empresa WHERE status_empresa = 'ATIVO' ORDER BY nome_empresa ASC;")
                resultado_empresas = conn.fetchall()

                for empresa in resultado_empresas:
                    info_empresas = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">{empresa[1]}<div id="div_id{contador}"><ul><li><br>ID: {empresa[0]}<br>CNPJ: {empresa[2]}<br>LOCALIZAÇÃO: {empresa[3]}<br>PORTE: {empresa[4]}<br>DESCRIÇÃO: {empresa[5]}<br>STATUS: {empresa[6]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{url_for('delete_empresa', empresa_id=empresa[0])}" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div></li>'''
                    empresas.append(info_empresas)
                    contador += 1

                # Ver candidatos
                conn.execute("SELECT * FROM candidato WHERE status_candidato = 'ATIVO' ORDER BY nome_candidato ASC;")
                resultado_candidatos = conn.fetchall()

                for candidato in resultado_candidatos:
                    info_candidato = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">{candidato[1]}<div id="div_id{contador}"><ul><li><br>ID: {candidato[0]}<br>CPF: {candidato[2]}<br>TELEFONE: {candidato[3]}<br>ENDEREÇO: {candidato[4]}<br>E-MAIL: {candidato[5]}<br>STATUS: {candidato[6]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{url_for('delete_candidato', candidato_id=candidato[0])}" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div></li>'''
                    candidatos.append(info_candidato)
                    contador += 1

                # Ver aplicações
                conn.execute("SELECT * FROM aplicacao WHERE status_aplicacao = 'ATIVO' ORDER BY data_aplicacao ASC;")
                resultado_aplicacoes = conn.fetchall()

                for aplicacao in resultado_aplicacoes:
                    conn.execute("SELECT nome_vaga FROM vagas WHERE id_vaga = %s;", (aplicacao[2],))
                    nome_vaga = conn.fetchone()

                    conn.execute("SELECT nome_candidato FROM candidato WHERE id_candidato = %s;", (aplicacao[1],))
                    nome_candidato = conn.fetchone()

                    nome_vaga_text = nome_vaga[0] if nome_vaga else 'Desconhecida'
                    nome_candidato_text = nome_candidato[0] if nome_candidato else 'Desconhecido'

                    info_aplicacao = f'''<li class="ver" onclick="mostrarDiv('div_id{contador}')">VAGA: {nome_vaga_text} | CANDIDATO: {nome_candidato_text}<div id="div_id{contador}"><ul><li><br>ID: {aplicacao[0]}<br>ID CANDIDATO: {aplicacao[1]}<br>ID VAGA: {aplicacao[2]}<br>DATA APLICAÇÃO: {aplicacao[3]}<br>STATUS: {aplicacao[4]}</li></ul>
                    <ul class="forms">
                    <li>
                    <form style="display:inline;">
                    <button type="submit">Editar</button>
                    </form>
                    </li>
                    <li>
                    <form action="{url_for('delete_aplicacao', aplicacao_id=aplicacao[0])}" method="POST" style="display:inline;">
                    <button type="submit">Excluir</button>
                    </form>
                    </li>
                    </ul></div></li>'''
                    aplicacoes.append(info_aplicacao)
                    contador += 1

    except Error as erro:
        logging.error(f'Erro ao buscar dados: {erro}')
        vagas.append('Erro ao buscar vagas.')
        empresas.append('Erro ao buscar empresas.')
        candidatos.append('Erro ao buscar candidatos.')
        aplicacoes.append('Erro ao buscar aplicações.')

    return render_template('index.html', username=session.get('username'), vagas_ver=vagas, empresas_ver=empresas, candidato_ver=candidatos, aplicacao_ver=aplicacoes)

@app.route('/delete_vaga/<int:vaga_id>', methods=['POST'])
def delete_vaga(vaga_id):
    try:
        with get_db_connection() as conexao_bd:
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
        with get_db_connection() as conexao_bd:
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
        with get_db_connection() as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE aplicacao SET status_aplicacao = 'INATIVO' WHERE id_candidato = %s", (candidato_id,))
                conn.execute("UPDATE candidato SET status_candidato = 'INATIVO' WHERE id_candidato = %s", (candidato_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar candidato: {e}')
    return redirect(url_for('homepage'))

@app.route('/delete_aplicacao/<int:aplicacao_id>', methods=['POST'])
def delete_aplicacao(aplicacao_id):
    try:
        with get_db_connection() as conexao_bd:
            with conexao_bd.cursor() as conn:
                conn.execute("UPDATE aplicacao SET status_aplicacao = 'INATIVO' WHERE id_aplicacao = %s", (aplicacao_id,))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao deletar aplicação: {e}')
    return redirect(url_for('homepage'))

@app.route('/add_vaga', methods=['GET', 'POST'])
def add_vaga():
    if request.method == 'POST':
        try:
            with get_db_connection() as conexao_bd:
                with conexao_bd.cursor() as conn:
                    nome_vaga = request.form['nome_vaga']
                    id_empresa = request.form['id_empresa']
                    funcao = request.form['funcao']
                    salario = request.form['salario']
                    status = 'ATIVO'

                    conn.execute('INSERT INTO vagas (id_empresa, nome_vaga, funcao, salario, status_vaga) VALUES (%s, %s, %s, %s, %s)',
                                 (id_empresa, nome_vaga, funcao, salario, status))
                    conexao_bd.commit()
        except Error as e:
            logging.error(f'Erro ao adicionar vaga: {e}')
            return render_template('add_vaga.html', error='Erro ao adicionar a vaga.')
        return redirect(url_for('homepage'))
    return render_template('add_vaga.html')


@app.route('/add_empresa', methods=['POST'])
def add_empresa():
    try:
        with get_db_connection() as conexao_bd:
            with conexao_bd.cursor() as conn:
                nome_empresa = request.form['nome_empresa']
                cnpj_empresa = request.form['cnpj_empresa']
                localizacao_empresa = request.form['localizacao_empresa']
                porte_empresa = request.form['porte_empresa']
                descricao_empresa = request.form['descricao_empresa']
                status_empresa = request.form['status_empresa']  # Certifique-se de que isso é enviado corretamente

                conn.execute('INSERT INTO empresas (nome_empresa, cnpj_empresa, localizacao_empresa, porte_empresa, descricao_empresa, status_empresa) VALUES (%s, %s, %s, %s, %s, %s)',
                             (nome_empresa, cnpj_empresa, localizacao_empresa, porte_empresa, descricao_empresa, status_empresa))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao adicionar empresa: {e}')
        return render_template('add_empresa.html', error='Erro ao adicionar a empresa.')
    
    return redirect(url_for('homepage'))

@app.route('/add_candidado', methods=['POST'])
def add_candidato():
    try:
        with get_db_connection() as conexao_bd:
            with conexao_bd.cursor() as conn:
                nome_candidato = request.form['nome_candidato']
                cpf_candidato = request.form['cpf_candidato']
                telefone_candidato = request.form['telefone_candidato']
                endereco_candidato = request.form['endereco_candidato']
                email_candidato = request.form['email_candidato']
                status_candidato = request.form['status_candidato']

                conn.execute('INSERT INTO candidato (nome_candidato, cpf_candidato, telefone_candidato, endereco_candidato, email_candidato, status_candidato) VALUES (%s, %s, %s, %s, %s, %s)',
                             (nome_candidato, cpf_candidato, telefone_candidato, endereco_candidato, email_candidato, status_candidato))
                conexao_bd.commit()
    except Error as e:
        logging.error(f'Erro ao adicionar candidato: {e}')
        return render_template('add_candidato.html', error='Erro ao adicionar o candidato.')
    
    return redirect(url_for('homepage'))




if __name__ == '__main__':
    app.run(debug=True)

