import os
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MySQL CONFIGURATIONS
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Tuca1234'
app.config['MYSQL_DATABASE_DB'] = 'clinicas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ROTAS DO MENU

@app.route('/', methods=['POST','GET'])
def listar():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select razao_social, cnpj, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, responsavel_tecnico from tbl_clinicas')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_clinicas.html', datas=data)


@app.route('/dentistas', methods=['POST','GET'])
def listardentista():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, cro, especialidades from tbl_dentistas')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_dentistas.html', datasdentistas=data)

@app.route("/pacientes", methods=['POST','GET'])
def listarpacientes():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone from tbl_pacientes')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_pacientes.html', dataspacientes=data)

@app.route("/consultas", methods=['POST','GET'])
def consultas():
    return render_template("lista_consultas.html")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ROTAS CLÍNICAS

# ROTA PARA CADASTRAR CLÍNICA

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
    return render_template('nova_clinica.html', msg='Dados gravados com sucesso. Desejar cadastrar mais uma Clínica? Preencha o formulário acima novamente.')

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


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ROTAS DENTISTAS

# ROTA PARA CADASTRAR DENTISTAS

@app.route("/cadastrardentista", methods=["POST"])
def cadastrar_dentista():
    return render_template("novo_dentista.html")

# ROTA PARA GRAVAR DENTISTAS

@app.route('/gravardentista', methods=['POST','GET'])
def gravar_dentista():
    nome = request.form['nome']
    cpf = request.form['cpf']
    logradouro = request.form['logradouro']
    complemento = request.form['complemento']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']
    email = request.form['email']
    telefone = request.form['telefone']
    cro = request.form['cro']
    especialidades = request.form['especialidades']
    
    if nome and cpf and logradouro and complemento and bairro and cidade and estado and cep and email and telefone and cro and especialidades:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('insert into tbl_dentistas (nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, cro, especialidades) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, cro, especialidades))
        conn.commit()
    return render_template('novo_dentista.html', msg='Dados gravados com sucesso. Desejar cadastrar mais um Dentista? Preencha o formulário acima novamente.')

# ROTA PARA RETORNAR DA PÁGINA GRAVAR DENTISTAS

@app.route("/retornardentista", methods=["POST"])
def retornar_dentista():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone, cro, especialidades from tbl_dentistas')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_dentistas.html', datasdentistas=data)

# ROTA PARA PARA DELETAR UM DENTISTA

@app.route("/deletardentista/<string:nome>")
def deletardentista(nome):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_dentistas WHERE nome=%s", (nome,))
        conn.commit()
        return redirect('/dentistas')  
    except:
        return "Desculpe. Algo deu errado. Contacte o administrador do sistema"

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ROTAS PACIENTES

# ROTA PARA CADASTRAR PACIENTES

@app.route("/cadastrarpaciente", methods=["POST"])
def cadastrar_pacientes():
    return render_template("novo_paciente.html")

# ROTA PARA GRAVAR PACIENTE

@app.route('/gravarpaciente', methods=['POST','GET'])
def gravar_paciente():
    nome = request.form['nome']
    cpf = request.form['cpf']
    logradouro = request.form['logradouro']
    complemento = request.form['complemento']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']
    email = request.form['email']
    telefone = request.form['telefone']
    
    if nome and cpf and logradouro and complemento and bairro and cidade and estado and cep and email and telefone:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('insert into tbl_pacientes (nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone))
        conn.commit()
    return render_template('novo_paciente.html', msg='Dados gravados com sucesso. Desejar cadastrar mais um paciente? Preencha o formulário acima novamente.')

# ROTA PARA RETORNAR DA PÁGINA GRAVAR PACIENTES

@app.route("/retornarpaciente", methods=["POST"])
def retornar_paciente():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select nome, cpf, logradouro, complemento, bairro, cidade, estado, cep, email, telefone from tbl_pacientes')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista_pacientes.html', dataspacientes=data)

# ROTA PARA PARA DELETAR UM PACIENTE

@app.route("/deletarpaciente/<string:nome>")
def deletarpaciente(nome):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_pacientes WHERE nome=%s", (nome,))
        conn.commit()
        return redirect('/pacientes')  
    except:
        return "Desculpe. Algo deu errado. Contacte o administrador do sistema"

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=5008)

