import os
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL CONFIGURATIONS
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Tuca1234'
app.config['MYSQL_DATABASE_DB'] = 'clinicas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# ROTA DA PÁGINA INICIAL DE CONSULTAR CLÍNICAS

@app.route('/', methods=['POST','GET'])
def listar():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico from tbl_clinicas')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_clinicas.html', datas=data)

# ROTAS DO MENU

@app.route("/dentistas", methods=["POST"])
def dentistas():
    return render_template("lista_dentistas.html")

@app.route("/pacientes", methods=["POST"])
def pacientes():
    return render_template("lista_pacientes.html")

@app.route("/consultas", methods=["POST"])
def consultas():
    return render_template("lista_consultas.html")

@app.route("/relatorios", methods=["POST"])
def relatorios():
    return render_template("lista_relatorios.html")

# ROTA DA PÁGINA CADASTRAR CLÍNICAS

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    return render_template("nova_clinica.html")

# ROTA PARA GRAVAR CLÍNICAS

@app.route('/gravar', methods=['POST','GET'])
def gravar():
    razao_social = request.form['razao_social']
    cnpj = request.form['cnpj']
    logradouro = request.form['logradouro']
    complemento = request.form['complemento']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']
    email = request.form['email']
    telefone = request.form['telefone']
    responsavel_tecnico = request.form['responsavel_tecnico']

    if razao_social and cnpj and logradouro and complemento and bairro and cidade and estado and cep and email and telefone and responsavel_tecnico:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('insert into tbl_clinicas (razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico))
        conn.commit()
    return render_template('nova_clinica.html', msg='Dados gravados com sucesso. Desejar criar mais uma Clínica? Preencha o formulário acima novamente.')

# ROTA PARA RETORNAR DA PÁGINA GRAVAR CLÍNICAS

@app.route("/retornar", methods=["POST"])
def retornar():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico from tbl_clinicas')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_clinicas.html', datas=data)

# ROTA PARA PARA DELETAR UMA CLÍNICA

@app.route("/deletar/<string:razao_social>")
def deletar(razao_social):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_clinicas WHERE razao_social=%s", (razao_social,))
        conn.commit()
        return redirect('/')  
    except:
        return "Desculpe. Algo deu errado. Contacte o administrador do sistema"

# ROTA PARA CONSULTAR UMA CLÍNICA

@app.route("/consultar/<string:razao_social>")
def consultar(razao_social):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT FROM tbl_clinicas razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico WHERE razao_social=%s', (razao_social))
        data = cursor.fetchall()
        conn.commit()
        return render_template('edita_clinica.html', datas=data)
    except:
        return "Desculpe. Algo deu errado. Contacte o administrador do sistema"
    
    
if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=5008)

