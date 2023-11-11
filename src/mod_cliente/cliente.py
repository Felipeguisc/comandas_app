from flask import Blueprint, render_template, request, redirect, url_for
import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE
from funcoes import Funcoes

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

@bp_cliente.route('/')
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
        print('Começou insert Cliente')
        # dados enviados via FORM
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        print('Começou parse diaFiado')
        compraFiado = request.form['compraFiado']
        print('Começou parse diaFiado')
        diaFiado_string = request.form['diaFiado']
        # Convert the string to bytes using UTF-8 encoding
        diaFiado_bytes = diaFiado_string.encode('utf-8').hex()
        
        #senha = request.form['senha’]
        senha = Funcoes.cifraSenha(request.form['senha'])
        print('COmeçou monta payload')
        # monta o JSON para envio a API
        payload = {'id': 0, 
                   'nome': nome, 
                   'cpf': cpf, 
                   'telefone': telefone, 
                   'compraFiado': compraFiado, 
                   'diaFiado' : diaFiado_bytes, 
                   'senha': senha}
        
        print('id: ', 0, 
                   'nome: ', nome, 
                   'cpf: ', cpf, 
                   'telefone: ', telefone, 
                   'compraFiado: ', compraFiado, 
                   'diaFiado; ', diaFiado_bytes, 
                   'senha: ', senha )
        
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