import flask
import sqlite3

app = flask.Flask(__name__)

@app.route("/")
def homePage():
    return flask.render_template('homepage.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if  flask.request.method == 'POST':
        user_name = flask.request.form.get("username")
        password = flask.request.form.get("password")
        type =  flask.request.form.get("type")

        print(user_name, password, type)

        pass

    return flask.render_template('login_user.html')

@app.route("/signup", methods = ["GET", "POST"])
def register():

    erro_mensage = f''

    if  flask.request.method == 'POST':
        try:
            

            account_type = flask.request.form.get('type')
            nome_sobrenome = flask.request.form.get('nome')
            username = flask.request.form.get('username')
            data_nascimento = flask.request.form.get('data_nascimento')
            cpf = flask.request.form.get('cpf')
            email  = flask.request.form.get('email')
            confirma_email = flask.request.form.get('confirma_email')
            senha = flask.request.form.get('senha')
            confirma_senha = flask.request.form.get('confirma_senha')

            if email  != confirma_email:
                erro_mensage += "Emails não conferem"
                if senha != confirma_senha:
                    erro_mensage += " \nSenhas não conferem"
            elif senha != confirma_senha:
                    erro_mensage += " \nSenhas não conferem"
                
        except ValueError as erro:
            erro_mensage +=  "\n" + str(erro)
        print(erro_mensage)

    return flask.render_template('register_user.html', erro_mensage = erro_mensage)


@app.route("/contatos")
def contato():
    return flask.render_template('contato.html')

@app.route("/equipe")
def equipe():
    return flask.render_template('equipe.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')