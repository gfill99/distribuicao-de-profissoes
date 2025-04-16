# Importa bibliotecas padrão para manipulação de sistema e banco de dados
import sys
import os
import duckdb as db

# Pega o diretório onde está o próprio config.py (a raiz do projeto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Função que adiciona os caminhos das pastas do projeto ao sys.path
def mapeia_pastas():
    pastas = [
        'ingestao_de_dados/utils', 
        'ingestao_de_dados/database', 
        'ingestao_de_dados/origens', 
        'ingestao_de_dados/tests', 
        'analise_de_dados/utils',  
        'analise_de_dados/app',  
        'analise_de_dados/result' 
        'IA_generativa/utils', 
        'IA_generativa/app'  
    ]
    # Adiciona cada pasta no sys.path para que os módulos possam ser importados de qualquer lugar do projeto
    for p in pastas:
        caminho = os.path.join(BASE_DIR, p)
        sys.path.append(caminho)

# Função que cria uma conexão com o banco de dados DuckDB utilizado no projeto
# O caminho relativo leva até o arquivo .db na pasta ingestao_de_dados/database
def criar_conexao_db():
    con = db.connect("../../ingestao_de_dados/database/db_distribuicao_profissoes.db")
    return con