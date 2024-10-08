import flask

app = flask.Flask(__name__)

@app.route("/")
def homePage():
    return flask.render_template('homepage.html')
@app.route("/login")
def login():
    return flask.render_template('login_user.html')
@app.route("/signup")
def register():
    return flask.render_template('register_user.html')
@app.route("/contatos")
def contato():
    return flask.render_template('contato.html')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')