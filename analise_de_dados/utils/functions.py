import duckdb as db
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

####################### MAPEANDO E CRIANDO CONEXÃO COM BANCO DE DADOS #######################

sys.path.append(os.path.abspath('../..'))

import configs as cf
cf.mapeia_pastas()

def criar_conexao_db():
    con = db.connect("../../ingestao_de_dados/database/db_distribuicao_profissoes.db")
    return con


####################### FUNÇÕES QUE REALIZAM MANIPULAÇÃO DE DADOS #######################


def contar_profissionais(con, genero_m, genero_f, profissao):    
    coluna_total = f"total_{profissao}"
    df = con.execute(f"""
        SELECT nome_estado, 
               ({genero_m.upper()}_{profissao} + {genero_f.upper()}_{profissao}) AS {coluna_total}
        FROM df_estados_profissoes
        ORDER BY {coluna_total} DESC
        LIMIT 7
    """).df()
    return df


def distribuir_profissao_por_genero(con, genero, total_genero, nomes_femininos=False):
    if nomes_femininos:
        nomes_colunas = {
            'advogados': 'advogadas',
            'contadores': 'contadoras',
            'engenheiros': 'engenheiras',
            'psicologos': 'psicologas'
        }
    else:
        nomes_colunas = {
            'advogados': 'advogados',
            'contadores': 'contadores',
            'engenheiros': 'engenheiros',
            'psicologos': 'psicologos'
        }

    query = f"""
        SELECT 
            nome_estado,
            SUM({genero}_advogados) AS {nomes_colunas['advogados']},
            SUM({genero}_contadores) AS {nomes_colunas['contadores']},
            SUM({genero}_engenheiros) AS {nomes_colunas['engenheiros']},
            SUM({genero}_psicologos) AS {nomes_colunas['psicologos']},
            SUM({genero}_advogados + {genero}_contadores + {genero}_engenheiros + {genero}_psicologos) AS {total_genero}
        FROM df_estados_profissoes
        GROUP BY nome_estado
        ORDER BY {total_genero} DESC
        LIMIT 7
    """
    return con.execute(query).df()

def ordena_query_profissão(con, genero, profissao):
	profissao_genero = con.execute(f"""
		SELECT nome_estado, {genero}_{profissao} AS total
		FROM df_estados_profissoes
		ORDER BY total DESC
		LIMIT 7
		""").df()
	return profissao_genero


####################### FUNÇÕES QUE REALIZAM CRIAÇÃO DE GRÁFICOS #######################

def plotar_maiores_estados_profissoes(con, profissoes, cores=None):
    """
    Gera subplots horizontais mostrando os 5 estados com mais profissionais por profissão.

    Parâmetros:
    - con: conexão ativa do DuckDB
    - profissoes: lista de strings com os nomes das profissões (ex: ['advogados', 'contadores'])
    - cores: lista de cores na mesma ordem da lista de profissões (opcional)
    """
    if cores is None:
        cores = ['#7f8c8d'] * len(profissoes)

    dados = []
    for i, profissao in enumerate(profissoes):
        df = contar_profissionais(con, 'M', 'F', profissao)
        coluna_total = f'total_{profissao}'
        cor = cores[i] if i < len(cores) else '#7f8c8d'
        dados.append((df, coluna_total, profissao.capitalize(), cor))

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Top Estados com mais profissionais por profissão', fontsize=16)

    for ax, (df, coluna, titulo, cor) in zip(axs.flat, dados):
        ax.barh(df['nome_estado'], df[coluna], color=cor)
        ax.set_title(titulo)
        ax.invert_yaxis()
        for i, v in enumerate(df[coluna]):
            ax.text(v + max(df[coluna]) * 0.01, i, f'{int(v):,}'.replace(',', '.'), va='center', fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def plotar_distribuicao_genero(df, profissoes, titulo, cor_legenda, genero_label):
    estados = df['nome_estado'].tolist()
    valores = [df[prof].values for prof in profissoes]
    
    x = np.arange(len(estados))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, (label, cor) in enumerate(zip(profissoes, cor_legenda)):
        bars = ax.bar(x + i * width, valores[i], width, label=label.capitalize(), color=cor)
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height):,}'.replace(',', '.'),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    ax.set_ylabel(f'Quantidade de profissionais ({genero_label})')
    ax.set_title(titulo)
    ax.set_xticks(x + width * (len(profissoes) - 1) / 2)
    ax.set_xticklabels(estados)
    ax.legend()
    plt.tight_layout()
    plt.show()

####################### FUNÇÃO PARA SALVAR ARQUIVOS JSON FINAIS #######################


def salvar_json(dataframes, pasta_resultados='../result'):
    # Caminho correto para a pasta result
    caminho_pasta = os.path.join(os.getcwd(), pasta_resultados)
    
    # Salvando os dataframes como arquivos JSON
    for nome, df in dataframes.items():
        # Definindo o caminho completo para o arquivo JSON
        caminho_arquivo = os.path.join(caminho_pasta, f"{nome}.json")
        
        # Convertendo o dataframe para JSON e salvando
        json_data = df.to_json(orient='records', force_ascii=False, indent=4)
        
        # Gravando o JSON no arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print(f"Arquivo {nome}.json salvo em {caminho_arquivo}")