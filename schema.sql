CREATE TABLE IF NOT EXISTS tb_instituicao_ensino (
    id SERIAL PRIMARY KEY,
    no_entidade VARCHAR(255) NOT NULL,
    co_entidade VARCHAR(20) NOT NULL,
    no_uf VARCHAR(255) NOT NULL,
    sg_uf CHAR(2) NOT NULL,
    co_uf INTEGER NOT NULL,
    no_municipio VARCHAR(255) NOT NULL,
    co_municipio INTEGER NOT NULL,
    nu_ano_censo INTEGER NOT NULL,
    qt_mat_bas INTEGER NOT NULL,
    qt_mat_inf INTEGER NOT NULL,
    qt_mat_fund INTEGER NOT NULL,
    qt_mat_med INTEGER NOT NULL,
    qt_mat_prof INTEGER NOT NULL,
    qt_mat_eja INTEGER NOT NULL,
    qt_mat_esp INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS tb_usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    nascimento DATE,
    email VARCHAR(255)
);
