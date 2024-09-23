from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')




@app.route('/index')
def homepage():
    return render_template('index.html')




# EXEMPLO FEITO POR PROF/: TARIK
#@app.route('/')
# def homepage():
#     listaDeVagas = ([1, "Jorge", "Cabelereiro"], [2,"Matheus", "Assistente"], [3,"Maicão", "Pedreiro"])
#     return render_template('homepage.html', vagas=listaDeVagas)



# @app.route('/login', methods=['POST'])
# def validar():
#     nomeUsuario = request.form.get("username")
#     senhaUsuario = request.form.get("password")

#     if (nomeUsuario == "Teste" and senhaUsuario == "123"):
#         return "Parabéns, acesso autorizado"
    
#     return "Acesso negado"


if __name__ == '__main__':
    app.run(debug=True)