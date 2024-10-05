import flask

app = flask(__name__)

@app.route("/")
def homePage():
    return flask.render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)