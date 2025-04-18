# Importação das bibliotecas necessárias
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

####################### MAPEANDO E CRIANDO CONEXÃO COM BANCO DE DADOS #######################

# Adicionando o caminho raiz ao sys.path para facilitar importações de outros diretórios do projeto
sys.path.append(os.path.abspath('../..'))

# Importa configurações e funções auxiliares
import configs as cf
cf.mapeia_pastas()

# Cria a conexão com o banco de dados DuckDB
con = cf.criar_conexao_db()

####################### FUNÇÕES QUE REALIZAM MANIPULAÇÃO DE DADOS #######################

# Função que conta a quantidade total de profissionais (masculino + feminino) por profissão
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

# Função que distribui as quantidades de profissionais por gênero e profissão, por estado
# Possui a opção de personalizar os nomes das colunas no caso de nomes femininos
def distribuir_profissao_por_genero(con, genero, total_genero):
    # Define o nome das colunas conforme o gênero selecionado
    if genero == "F":
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

####################### FUNÇÕES QUE REALIZAM CRIAÇÃO DE GRÁFICOS #######################

# Função que plota gráficos de barras horizontais para os estados com mais profissionais por profissão
# Permite customizar as cores das barras
def plotar_maiores_estados_profissoes(con, profissoes, cores=None):
    """
    Gera subplots horizontais mostrando os 5 estados com mais profissionais por profissão.

    Parâmetros:
    - con: conexão ativa do DuckDB
    - profissoes: lista de strings com os nomes das profissões (ex: ['advogados', 'contadores'])
    - cores: lista de cores na mesma ordem da lista de profissões (opcional)
    """
    # Se não for especificada nenhuma cor, define todas como cinza padrão
    if cores is None:
        cores = ['#7f8c8d'] * len(profissoes)

    # Lista para armazenar os dados que serão plotados
    dados = []
    for i, profissao in enumerate(profissoes):
        df = contar_profissionais(con, 'M', 'F', profissao)
        coluna_total = f'total_{profissao}'
        cor = cores[i] if i < len(cores) else '#7f8c8d'
        dados.append((df, coluna_total, profissao.capitalize(), cor))

     # Cria a estrutura dos subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Top Estados com mais profissionais por profissão', fontsize=16)

    # Preenche cada subplot com os dados correspondentes
    for ax, (df, coluna, titulo, cor) in zip(axs.flat, dados):
        ax.barh(df['nome_estado'], df[coluna], color=cor)
        ax.set_title(titulo)
        ax.invert_yaxis() # Coloca o maior valor no topo
        # Adiciona as quantidades de profissionais ao lado das barras
        for i, v in enumerate(df[coluna]):
            ax.text(v + max(df[coluna]) * 0.01, i, f'{int(v):,}'.replace(',', '.'), va='center', fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Função que plota gráfico de barras agrupadas para mostrar a distribuição de profissionais por gênero e profissão
def plotar_distribuicao_genero(df, profissoes, titulo, cor_legenda, genero_label):
    # Extrai os estados e os valores das colunas de cada profissão
    estados = df['nome_estado'].tolist()
    valores = [df[prof].values for prof in profissoes]
    
    # Define a posição das barras no eixo X e a largura delas
    x = np.arange(len(estados))
    width = 0.2

    fig, ax = plt.subplots(figsize=(14, 8))

    # Adiciona as barras para cada profissão e estado
    for i, (label, cor) in enumerate(zip(profissoes, cor_legenda)):
        bars = ax.bar(x + i * width, valores[i], width, label=label.capitalize(), color=cor)
        # Adiciona os valores acima de cada barra
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

# Função que salva múltiplos DataFrames em arquivos JSON no diretório especificado
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