from psycopg2 import Error as DatabaseError

from helpers.database import get_connection
from models.instituicaoensino import InstituicaoEnsino


class InstituicaoEnsinoRepository():

    def row_to_instituicao(self, row):
        return InstituicaoEnsino(
            id=row[0],
            no_entidade=row[1],
            co_entidade=row[2],
            no_uf=row[3],
            sg_uf=row[4],
            co_uf=row[5],
            no_municipio=row[6],
            co_municipio=row[7],
            nu_ano_censo=row[8],
            qt_mat_bas=row[9],
            qt_mat_inf=row[10],
            qt_mat_fund=row[11],
            qt_mat_med=row[12],
            qt_mat_prof=row[13],
            qt_mat_eja=row[14],
            qt_mat_esp=row[15],
            created=row[16]
        )

    def getInstituicoes(self, limit, offset):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created_at AS created
                FROM tb_instituicao_ensino
                WHERE deleted_at IS NULL
                ORDER BY id
                LIMIT %s OFFSET %s
            """, (limit, offset))
            rows = cursor.fetchall()

            return [self.row_to_instituicao(row) for row in rows]
        except DatabaseError:
            connection.rollback()
            raise

    def countInstituicoes(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(id)
                FROM tb_instituicao_ensino
                WHERE deleted_at IS NULL
            """)
            return cursor.fetchone()[0]
        except DatabaseError:
            connection.rollback()
            raise

    def getInstituicao(self, id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created_at AS created
                FROM tb_instituicao_ensino
                WHERE id = %s AND deleted_at IS NULL
            """, (id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return self.row_to_instituicao(row)
        except DatabaseError:
            connection.rollback()
            raise

    def inserirInstituicao(self, data):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
            """, (
                data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data[
                    "co_uf"], data["no_municipio"], data["co_municipio"], data["nu_ano_censo"],
                data["qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data[
                    "qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"]
            ))
            resultset = cursor.fetchone()

            connection.commit()

            return InstituicaoEnsino(**data, id=resultset[0], created=resultset[1])
        except DatabaseError:
            connection.rollback()
            raise

    def atualizarInstituicao(self, id, data):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE tb_instituicao_ensino
                SET no_entidade = %s, co_entidade = %s, no_uf = %s, sg_uf = %s, co_uf = %s, no_municipio = %s, co_municipio = %s, nu_ano_censo = %s, qt_mat_bas = %s, qt_mat_inf = %s, qt_mat_fund = %s, qt_mat_med = %s, qt_mat_prof = %s, qt_mat_eja = %s, qt_mat_esp = %s
                WHERE id = %s AND deleted_at IS NULL
            """, (
                data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data[
                    "co_uf"], data["no_municipio"], data["co_municipio"], data["nu_ano_censo"],
                data["qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data[
                    "qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"], id
            ))
            atualizada = cursor.rowcount > 0

            if not atualizada:
                connection.rollback()
                return None

            connection.commit()

            return self.getInstituicao(id)
        except DatabaseError:
            connection.rollback()
            raise

    def softDeleteInstituicao(self, id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE tb_instituicao_ensino
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = %s AND deleted_at IS NULL
            """, (id,))
            removida = cursor.rowcount > 0

            connection.commit()

            return removida
        except DatabaseError:
            connection.rollback()
            raise
