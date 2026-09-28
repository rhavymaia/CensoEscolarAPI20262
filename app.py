from flask import Flask, request, jsonify
from marshmallow import ValidationError


from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema
from helpers.file.json import read
from helpers.database import get_connection

InstituicaoEnsinoSchema = InstituicaoEnsinoSchema()


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


app = Flask(__name__)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200

# /instituicoesensino?co_inep=123456


@app.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsinoReponse = []
    # Abrir a conexão com o banco de dados.
    connection = get_connection()
    cursor = connection.cursor()
    # Executar as DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino')
    dataset = cursor.fetchall()
    for row in dataset:
        id = row[0]
        no_entidade = row[1]
        co_entidade = row[2]
        qt_mat_bas = row[9]
        print(f'{id}, {no_entidade}, {co_entidade}, {qt_mat_bas}')
        instituicaoEnsino = InstituicaoEnsino(
            id, no_entidade, co_entidade, qt_mat_bas)
        # Transformação dos dados
        insituicoesEnsinoReponse.append(instituicaoEnsino.toDict())

    # Responder/retorna os dados ao cliente
    return insituicoesEnsinoReponse, 200


@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):
    insituicaoEnsinoReponse = None
    # Abrir a conexão com o banco de dados.
    connection = get_connection()
    cursor = connection.cursor()
    # Executar as DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino WHERE id = ?', (id,))
    row = cursor.fetchone()
    if row is not None:
        id = row[0]
        no_entidade = row[1]
        co_entidade = row[2]
        qt_mat_bas = row[9]
        print(f'{id}, {no_entidade}, {co_entidade}, {qt_mat_bas}')
        insituicaoEnsinoReponse = InstituicaoEnsino(
            id, no_entidade, co_entidade, qt_mat_bas)
    else:
        return {'mensagem': 'Instituição de ensino não encontrada'}, 404

        # Responder/retorna os dados ao cliente
    return insituicaoEnsinoReponse.toDict(), 200


@app.post("/instituicoesensino")
def postInstituicoes():
    # Entrada do dado em Json.
    # Validação.
    try:
        data = InstituicaoEnsinoSchema.load(request.get_json())

        # Inserção do registro no banco de dados
        no_entidade = data.get("no_entidade")
        co_entidade = data.get("co_entidade")
        no_uf = data.get("no_uf")
        sg_uf = data.get("sg_uf")
        co_uf = data.get("co_uf")
        no_municipio = data.get("no_municipio")
        co_municipio = data.get("co_municipio")
        nu_ano_censo = data.get("nu_ano_censo")
        qt_mat_bas = data.get("qt_mat_bas")
        qt_mat_inf = data.get("qt_mat_inf")
        qt_mat_fund = data.get("qt_mat_fund")
        qt_mat_med = data.get("qt_mat_med")
        qt_mat_prof = data.get("qt_mat_prof")
        qt_mat_eja = data.get("qt_mat_eja")
        qt_mat_esp = data.get("qt_mat_esp")

        # Abrir a conexão com o banco de dados.
        connection = get_connection()
        cursor = connection.cursor()
        # Executar as DML de consulta
        cursor.execute(f'INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id, created',
                       (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp))

        id = cursor.lastrowid
        resultset = cursor.fetchone()
        id = resultset[0]
        created = resultset[1]

        connection.commit()
    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

    # Retorno.
    # Dado de entrada com identificador.
    return {"id": id, "created": created}, 201


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
