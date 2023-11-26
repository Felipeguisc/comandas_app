from flask import Flask, session
import os

# import blueprint criado
from mod_error.error import bp_error
from mod_funcionario.funcionario import bp_funcionario
from mod_index.index import bp_index
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
from mod_login.login import bp_login

app = Flask(__name__)

# gerando uma chave randômica para secret_key
app.secret_key = os.urandom(12).hex()

# registro das rotas do blueprint
app.register_blueprint(bp_error)
app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_index)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_login)

if __name__ == "__main__":
    """ Inicia o aplicativo WEB Flask """
    app.run(host='0.0.0.0', port=5001, debug=True)
    
    
# ajuste SAMESITE
'''
O cookie "session" não tem o atributo "SameSite" com valor válido.
Em breve, cookies sem o atributo "SameSite" ou com valor inválido serão tratados como "Lax".
Significa que o cookie não será mais enviado em contextos de terceiros.
Se sua aplicação depender da disponibilidade deste cookie em tais contextos, adicione o
atributo "SameSite=None".
Saiba mais sobre o atributo "SameSite" em
https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite
'''
app.config.update(
SESSION_COOKIE_SAMESITE='None',
SESSION_COOKIE_SECURE='True'
)