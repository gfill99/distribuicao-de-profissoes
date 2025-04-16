# 📊 Distribuição de Profissões no Brasil

## 📌 Sobre o projeto

Este projeto tem como objetivo analisar a **distribuição de profissionais de diferentes áreas no Brasil**, segmentados por gênero e estado. As profissões analisadas são:

- Advogados
- Contadores
- Engenheiros
- Psicólogos

Além disso, o projeto conta com uma aplicação de **IA generativa** para a criação de insights ou relatórios a partir dos dados obtidos.

---

## 📂 Estrutura de pastas

```plaintext
distribuicao_profissao/  
└── distribuicao-de-profissao/  
    ├── analise_de_dados/  
    │   ├── app/  
    │   │   └── analise_de_dados.ipynb  
    │   ├── result/  
    │   │   ├── advogados.json  
    │   │   ├── contadores.json  
    │   │   ├── engenheiros.json  
    │   │   ├── psicologos.json  
    │   │   ├── maiores_estados_masculino.json  
    │   │   └── maiores_estados_feminino.json  
    │   └── utils/  
    │       └── functions.py  
    ├── IA_generativa/  
    │   ├── app/  
    │   │   └── IA_generativa.ipynb  
    │   └── utils/  
    │       ├── .env  
    │       └── prompts.txt  
    ├── ingestao_de_dados/  
    │   ├── app/  
    │   │   └── ingestao_de_dados.ipynb  
    │   ├── database/  
    │   │   ├── db_distribuicao_profissoes.db  
    │   │   └── ETL_tabelas.sql  
    │   ├── origens/  
    │   │   ├── tbl_advogados_brasil_2024.xlsx  
    │   │   ├── tbl_contadores_brasil_2024.xlsx  
    │   │   ├── tbl_engenheiros_brasil_2024.xlsx  
    │   │   ├── tbl_psicologos_brasil_2024.xlsx  
    │   │   └── tbl_estados_brasil.xlsx  
    │   ├── tests/  
    │   │   └── tests.ipynb  
    │   └── utils/  
    │       └── utils.json  
    ├── .gitignore  
    ├── configs.py  
    └── README.md
```

---

## ⚙️ Tecnologias e bibliotecas utilizadas

- Python
- DuckDB
- Pandas
- Matplotlib
- Groq API (para IA generativa)
- dotenv
- JSON
- Excel (para ingestão de dados)
- SQL (para manipulação de dados e criação de tabelas)
- Git (para controle de versão)

---

## 📊 Como executar o projeto

1. Clone este repositório:
   ```bash
   git clone [link-do-repo]
   cd distribuicao_profissao

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

3. Configure suas variáveis de ambiente:
    - **no arquivo ```.env``` (dentro de IA_generativa/utils).**

4. Execute os notebooks na seguinte ordem:

    - **ingestao_de_dados/app/ingestao_de_dados.ipynb**

    - **analise_de_dados/app/analise_de_dados.ipynb**

    - **IA_generativa/app/IA_generativa.ipynb**

---

## 📈 Resultados gerados

Os resultados das análises são armazenados na pasta analise_de_dados/result/ em formato JSON:

- advogados.json — distribuição de advogados por gênero e estado

- contadores.json — distribuição de contadores

- engenheiros.json — distribuição de engenheiros

- psicologos.json — distribuição de psicólogos

- maiores_estados_masculino.json — estados com mais profissionais homens

- maiores_estados_feminino.json — estados com mais profissionais mulheres

---

## 📌 Observações

- Os dados utilizados foram obtidos de fontes oficiais públicas e servem para fins educacionais e exploratórios. As fontes são:

  - **OAB — Quadro de Advogados**

  - **CONFEA — Profissionais por Gênero**

  - **CFP — Quantos Somos**

  - **CFC — Consulta por Região**

- A aplicação de IA generativa utiliza um modelo LLama da Meta, acessado via Groq API. É necessário configurar a chave de API no arquivo ```.env``` localizado em ```IA_generativa/utils/.env.```
