from dotenv import load_dotenv, find_dotenv
import os

# localiza o arquivo de .env
dotenv_file = find_dotenv()

# Carrega o arquivo .env
load_dotenv(dotenv_file)

# Configurações da APP
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")

# Configurações da API
URL_API = os.getenv("URL_API")
HEADERS_API = { 'X-API-Key': os.getenv("X_KEY"), 'X-Token': os.getenv("X_TOKEN")}

# Configuração dos endpoints
ENDPOINT_LOGIN = os.getenv("ENDPOINT_LOGIN")
ENDPOINT_FUNCIONARIO = os.getenv("ENDPOINT_FUNCIONARIO")
ENDPOINT_CLIENTE = os.getenv("ENDPOINT_CLIENTE")
ENDPOINT_PRODUTO = os.getenv("ENDPOINT_PRODUTO")

TEMPO_SESSION = os.getenv("TEMPO_SESSION")