from flask import  Flask, render_template, request, redirect, url_for

app =  Flask(__name__)

@app.route("/")

def teste():
    return main_pg(id_user = 1)

@app.route("/main_pg")
def main_pg( id_user = int):

    user = ID(id_user)
    data = user.get_id()
    print(data)

    return render_template("main.html", name = data[0]['nome'])

class ID():
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return [{'nome': 'Ricardo'}, {'account_type': 'candidato'}]

if __name__ == "__main__":

    app.run(debug = True, host = "0.0.0.0")
