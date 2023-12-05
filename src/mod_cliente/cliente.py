from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE
from funcoes import Funcoes
from mod_login. login import validaSessao

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

@bp_cliente.route('/')
@validaSessao
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=HEADERS_API, verify=False)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
    
        return render_template('formListaCliente.html', result=result)
    except Exception as e:
        print(e.args[0])
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/add-client', methods=['POST'])
def formCliente():
    return render_template('formCliente.html'), 200

@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compraFiado = request.form['compraFiado']
        diaFiado_string = request.form['diaFiado']
        # Convert the string to bytes using UTF-8 encoding
        diaFiado_bytes = diaFiado_string.encode('utf-8').hex()
        
        #senha = request.form['senha’]
        senha = Funcoes.cifraSenha(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'id': 0, 
                   'nome': nome, 
                   'cpf': cpf, 
                   'telefone': telefone, 
                   'compraFiado': compraFiado, 
                   'diaFiado' : diaFiado_bytes, 
                   'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route("/form-edit-cliente", methods=['POST'])
def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        # executa o verbo GET da API buscando somente o cliente selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, verify=False)
        print(response)
        result = response.json()
        print(result)
        if (response.status_code != 200):
            raise Exception(result[0])
        # renderiza o form passando os dados retornados
        return render_template('formCliente.html', result=result)
    
    except Exception as e:
        print(e.args[0])
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/edit', methods=['POST'])
def edit():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compraFiado = request.form['compraFiado']
        diaFiado_string = request.form['diaFiado']
        # Convert the string to bytes using UTF-8 encoding
        diaFiado_bytes = diaFiado_string.encode('utf-8').hex()
        #senha = request.form['senha’]
        senha = Funcoes.cifraSenha(request.form['senha'])
        
        # monta o JSON para envio a API
        payload = {'id': id_cliente, 
                   'nome': nome, 
                   'cpf': cpf, 
                   'telefone': telefone, 
                   'compraFiado': compraFiado, 
                   'diaFiado' : diaFiado_bytes,
                   'senha': senha}
        
        print(payload)
        
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        print(result)
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    except Exception as e:
        print(e.args[0])
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/delete', methods=['POST'])
def delete():
    try:
        print('Começou deletar cliente')
        print(request.form['id_cliente'])
        # dados enviados via FORM
        id_cliente = request.form['id_cliente']
        
        payload = {'id': id_cliente }
        print(id_cliente)
        
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        print(e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])

from mod_cliente.GeraPdf import PDF
    
@bp_cliente.route('/pdfTodos', methods=['POST'])
@validaSessao
def pdfTodos():
    print("PDF Cliente")
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('../pdfCliente.pdf')