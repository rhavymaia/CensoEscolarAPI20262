from flask import request, jsonify
from sqlite3 import OperationalError
from marshmallow import ValidationError


from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema, InstituicaoEnsinoCompactoSchema
from helpers.application import app
from helpers.file.json import read
from helpers.database import get_connection
from helpers.logger import logger

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)

instituicaoEnsinoCompactoSchema = InstituicaoEnsinoCompactoSchema(many=True)


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200


def row_to_instituicao(row):
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


# /instituicoesensino?co_inep=123456
@app.get("/instituicoesensino")
def get_all_instituicoes():

    logger.info("Listando as Insituições de Ensino")
    connection = get_connection()
    try:
        logger.info("Recuperando a conexão com o Banco de dados")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf,
                qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created
            FROM tb_instituicao_ensino
        """)
        rows = cursor.fetchall()

        instituicoes = [
            row_to_instituicao(row)
            for row in rows
        ]

        logger.info("Finalizando o processamento da Listagem")
        return jsonify(instituicoesEnsinoSchema.dump(instituicoes)), 200

    except OperationalError:
        logger.error("Erro no processamento dos dados no Banco de Dados")
        connection.rollback()
        raise


@app.get("/instituicoesensino/<int:id>")
def get_instituicao_by_id(id):

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created
            FROM tb_instituicao_ensino
            WHERE id = ?
        """, (id,))
        row = cursor.fetchone()

        if row is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404

        instituicao = row_to_instituicao(row)

        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 200
    except OperationalError:
        connection.rollback()
        raise


@app.post("/instituicoesensino")
def post_instituicao():

    try:
        data = InstituicaoEnsinoSchema.load(request.get_json())

        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id, created
        """, (
            data["no_entidade"], data["co_entidade"], data["no_uf"], data["sg_uf"], data["co_uf"], data["no_municipio"], data["co_municipio"], data["nu_ano_censo"], data[
                "qt_mat_bas"], data["qt_mat_inf"], data["qt_mat_fund"], data["qt_mat_med"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"]
        ))

        resultset = cursor.fetchone()
        id = resultset[0]
        created = resultset[1]

        connection.commit()

        instituicao = InstituicaoEnsino(**data, id=id, created=created)

        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 201

    except ValidationError as err:

        return {"erro": "Dados inválidos", "campos": err.messages}, 400

    except OperationalError:
        connection.rollback()
        raise


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes():
    pass


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes():
    pass


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()
