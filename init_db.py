import psycopg2

from helpers.application import app
from helpers.database import get_connection
from helpers.file.json import read

COLUNAS = [
    "no_entidade", "co_entidade", "no_uf", "sg_uf", "co_uf", "no_municipio", "co_municipio", "nu_ano_censo",
    "qt_mat_bas", "qt_mat_inf", "qt_mat_fund", "qt_mat_med", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp"
]


def criar_tabelas(connection):
    with open("schema.sql") as file, connection.cursor() as cursor:
        cursor.execute(file.read())


def popular_instituicoes(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tb_instituicao_ensino")
        if cursor.fetchone()[0] > 0:
            print("Tabela tb_instituicao_ensino já possui dados. Seed ignorado.")
            return

        instituicoes = read("instituicoes.json") or []
        registros = [
            tuple(str(i[c]) if c == "co_entidade" else i[c] for c in COLUNAS)
            for i in instituicoes
        ]

        cursor.executemany(f"""
            INSERT INTO tb_instituicao_ensino ({", ".join(COLUNAS)})
            VALUES ({", ".join(["%s"] * len(COLUNAS))})
        """, registros)
        print(f"{len(registros)} instituições inseridas.")


def main():
    with app.app_context():
        connection = get_connection()
        try:
            criar_tabelas(connection)
            popular_instituicoes(connection)
            connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            print(f"O PostgreSQL lançou uma exceção: {str(e)}")


if __name__ == "__main__":
    main()
