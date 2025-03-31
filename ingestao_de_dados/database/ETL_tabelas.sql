CREATE TABLE IF NOT EXISTS tbl_estados_brasil (
    id PRIMARY KEY AUTOINCREMENT,
    uf VARCHAR (50),
    nome_estado VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS tbl_advogados_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    id INTEGER REFERENCES tbl_estados_brasil(id), 
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_contadores_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    id INTEGER REFERENCES tbl_estados_brasil(id), 
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_engenheiros_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    id INTEGER REFERENCES tbl_estados_brasil(id), 
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_psicologos_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    id INTEGER REFERENCES tbl_estados_brasil(id), 
    feminino INTEGER, 
    masculino INTEGER
);