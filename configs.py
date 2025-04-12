import sys
import os

# Pega o diretório onde está o próprio config.py (a raiz do projeto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def mapeia_pastas():
    pastas = [
        'ingestao_de_dados/utils',
        'ingestao_de_dados/database',
        'ingestao_de_dados/origens',
        'ingestao_de_dados/tests',
        'analise_de_dados/utils',
        'analise_de_dados/app',
        'analise_de_dados/result'
    ]
    for p in pastas:
        caminho = os.path.join(BASE_DIR, p)
        sys.path.append(caminho)