from flask import Blueprint, render_template, request, redirect, url_for
import requests
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO
from funcoes import Funcoes

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

@bp_funcionario.route('/', methods=['GET', 'POST'])
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, verify=False)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])
    
        return render_template('formListaFuncionario.html', result=result)
    except Exception as e:
        print(e.args[0])
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/add-funcionario/', methods=['GET', 'POST'])
def formFuncionario():
    return render_template('formFuncionario.html'), 200

@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        #senha = request.form['senha’]
        senha = Funcoes.cifraSenha(request.form['senha'])

        # monta o JSON para envio a API
        payload = {'id': 0, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, json=payload, verify=False)
        print(response)
        result = response.json()
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    
    except Exception as e:
        return redirect(url_for('funcionario.formListaFuncionario', msgErro=e.args[0]))