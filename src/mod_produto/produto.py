from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from settings import HEADERS_API, ENDPOINT_PRODUTO
import base64
import re

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

@bp_produto.route('/')
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=HEADERS_API, verify=False)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
    
        return render_template('formListaProduto.html', result=result)
    except Exception as e:
        print(e.args[0])
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('add-produto', methods=['POST'])
def formProduto():
    return render_template('formProduto.html'), 200

@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        nome = request.form['nome']
        valorUnitario = request.form['valorUnitario']
        descricao = request.form['descricao']
        
        # converte a foto em base64
        foto = str(base64.b64encode(request.files['foto'].read()), "utf-8")

        # monta o JSON para envio a API
        payload = {'id' : 0, 
                   'nome': nome, 
                   'valorUnitario': valorUnitario, 
                   'descricao': descricao,
                   'foto': foto}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        
        #return redirect(url_for('produto.formListaProduto', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        print(e.args[0])
        #return render_template('formListaProduto.html', msgErro=e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_produto.route("/form-edit-produto", methods=['POST'])
def formEditProduto():
    try:
        # ID enviado via FORM
        id_produto = request.form['id']
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        
        payload = {'id': id_produto }
        
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        # renderiza o form passando os dados retornados
        return render_template('formProduto.html', result=result)
    
    except Exception as e:
        print(e.args[0])
        return render_template('formListaProduto.html', msgErro=e.args[0])
    
@bp_produto.route('/edit', methods=['POST'])
def edit():
    try:
        # dados enviados via FORM
        print("Começou atualiza produto")
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valorUnitario = request.form['valorUnitario']
        
        # converte a foto em base64
        foto = str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        # monta o JSON para envio a API
        payload = {'id': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valorUnitario': valorUnitario}
        
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_PRODUTO, headers=HEADERS_API, json=payload, verify=False)
        result = response.json()
        print(result)
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        
        #return redirect(url_for('produto.formListaProduto', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        # return render_template('formListaProduto.html', msgErro=e.args[0])
        print(e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])
    
    
@bp_produto.route('/delete', methods=['POST'])
def delete():
    try:
        print("Começou deleta produto")
        # dados enviados via FORM
        id_produto = request.form['id_produto']
        
        payload = {'id': id_produto }
        print(id_produto)
        
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, json=payload, headers=HEADERS_API, verify=False)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        
        # return redirect(url_for('produto.formListaProduto', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        # return render_template('formListaProduto.html', msgErro=e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])