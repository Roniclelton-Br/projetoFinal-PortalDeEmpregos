from flask import  Flask, render_template, request, redirect, url_for

app =  Flask(__name__)

@app.route("/")

def teste():
    return main_pg(name = str('ricardo'))

@app.route("/main_pg")
def main_pg( name = str):

    user = ID(name)
    data = user.get_id()
    #print(data)
    code = None

    if data[1]['account_type'] == 'candidato':
        if code is None:
            print("erro")
            codeErro = """
            <div class='erro-data'>
                <p>Nenhuma vaga registrada até o momento.
                </p>
            </div>"""
            print ('state-3')
            return render_template("main.html", name = data[0]['nome'].upper(), code = codeErro)

        print ('state-2')
        return render_template("main.html", name = data[0]['nome'].upper(), code = code)

        
    print ('state-1')
    return render_template("main.html", name = data[0]['nome'].upper())

class ID():
    def __init__(self, name):
        self.name = name 

    def get_id(self):
        return [{'nome': 'Ricardo'}, {'account_type': 'candidato'}, {'ID': '0'}]
    
    def search_bd(self):
        pass

    def edit_bd(self):
        pass

if __name__ == "__main__":

    app.run(debug = True, host = "0.0.0.0")
