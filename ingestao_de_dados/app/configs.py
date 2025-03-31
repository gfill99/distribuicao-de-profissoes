import sys
import os

# Função que mapeia as pastas necessárias para o projeto
def mapeia_pastas():
    # Lista das pastas que precisam ser acessadas: 'utils' e 'database'
    pastas = ['utils','database','origens','tests']
    # Laço para adicionar o caminho das pastas na variável sys.path
    for p in pastas:
        # sys.path é uma lista que contém todos os diretórios onde Python procura por módulos
        sys.path.append(os.path.abspath(f"../{p}"))