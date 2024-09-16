from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login')
def login():
    url_for('static', filename='stylesLogin.css')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5500)