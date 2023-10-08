from flask import Blueprint, render_template

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

@bp_produto.route('/')
def formListaIndex():
    return render_template('formListaProduto.html'), 200