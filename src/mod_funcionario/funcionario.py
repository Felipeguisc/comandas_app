from flask import Blueprint, render_template

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

@bp_funcionario.route('/', methods=['GET','POST'])
def formListaFuncionario():
    return render_template('formListaFuncionario.html'), 200

@bp_funcionario.route('/form-funcionario/', methods=['GET', 'POST'])
def formFuncionario():
    return render_template('formFuncionario.html'), 200