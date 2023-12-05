from flask import Blueprint, render_template, request, redirect, url_for, session
from funcoes import Funcoes
from functools import wraps
import requests
from settings import HEADERS_API, ENDPOINT_LOGIN
import json

bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')

@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formlogin.html")

@bp_login.route('/login', methods=['POST'])
def validalogin():
    try:
        # dados enviados via FORM
        cpf = request.form['cpf']
        senha = Funcoes.cifraSenha(request.form['senha'])

        # monta o JSON para envio a API
        payload = {'cpf': cpf, 'senha': senha}
        
        print(senha)

        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_LOGIN, headers=HEADERS_API, json=payload, verify=False)
        print(response.status_code)
        
        if (response.status_code == 200):
            # Convert JSON to Python object
            python_object = response.json()
            
            # registra usuário na sessão, armazenando o login do usuário
            session['login'] = python_object[0]
            
            # abre a aplicação na tela home
            return redirect(url_for('index.formIndex'))
        else:
            raise Exception("Falha de Login! Verifique seus dados e tente novamente!")

    except Exception as e:
        # retorna para a tela de login
        return redirect(url_for('login.login', msgErro=e.args[0]))
    
    
@bp_login.route("/logoff", methods=['GET'])
def logoff():
    # limpa um valor individual
    session.pop('login', None)
    # limpa toda sessão
    session.clear()
    # retorna para a tela de login
    return redirect(url_for('login.login'))

# valida se o usuário esta ativo na sessão
def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            # descarta os dados copiados da função original e retorna a tela de login
            return redirect(url_for('login.login', msgErro='Usuário não logado!'))
        else:
            # retorna os dados copiados da função original
            return f(*args, **kwargs)
    # retorna o resultado do if acima
    return decorated_function