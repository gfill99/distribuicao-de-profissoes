CREATE TABLE IF NOT EXISTS tbl_estados_brasil (
    id INTEGER PRIMARY KEY,
    uf VARCHAR (50),
    nome_estado VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS tbl_advogados_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY, 
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_contadores_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_engenheiros_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY,
    feminino INTEGER, 
    masculino INTEGER
);

CREATE TABLE IF NOT EXISTS tbl_psicologos_brasil_2024(
    estado VARCHAR (50) PRIMARY KEY, 
    feminino INTEGER, 
    masculino INTEGER
);