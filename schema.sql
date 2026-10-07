CREATE TABLE tb_instituicao_ensino (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_entidade TEXT NOT NULL,
    co_entidade TEXT NOT NULL,
    no_uf TEXT NOT NULL,
    sg_uf TEXT NOT NULL,
    co_uf INTEGER NOT NULL,
    no_municipio TEXT NOT NULL,
    co_municipio INTEGER NOT NULL,
    nu_ano_censo INTEGER NOT NULL,
    qt_mat_bas INTEGER NOT NULL,
    qt_mat_inf INTEGER NOT NULL,
    qt_mat_fund INTEGER NOT NULL,
    qt_mat_med INTEGER NOT NULL,
    qt_mat_prof INTEGER NOT NULL,
    qt_mat_eja INTEGER NOT NULL,
    qt_mat_esp INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    deleted_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS tb_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    nascimento TEXT,
    email TEXT
)