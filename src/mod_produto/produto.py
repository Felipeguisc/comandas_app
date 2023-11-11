from flask import Blueprint, render_template, request, redirect, url_for
import requests
from settings import HEADERS_API, ENDPOINT_PRODUTO
import base64

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
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    
    except Exception as e:
        print(e.args[0])
        return render_template('formListaProduto.html', msgErro=e.args[0])