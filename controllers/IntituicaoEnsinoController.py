from flask import Blueprint, request, jsonify
from psycopg2 import Error as DatabaseError
from marshmallow import ValidationError
from flask_restful import Resource

from models.instituicaoensino import InstituicaoEnsinoSchema, InstituicaoEnsinoCompactoSchema
from models.paginacao import PaginacaoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService
from helpers.logger import logger

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)
instituicaoEnsinoCompactoSchema = InstituicaoEnsinoCompactoSchema(many=True)
paginacaoSchema = PaginacaoSchema()


instituicao_ensino_bp = Blueprint(
    'instituicaoensino', __name__, url_prefix='/instituicoesensino')


class InstituicoesController(Resource):
    def get(self):
        try:
            logger.info("entrou no get do controlador")
            paginacao = paginacaoSchema.load(request.args)

            page = paginacao["page"]
            per_page = paginacao["per_page"]
            logger.info(
                f"Listando as Instituições de Ensino - página {page} com {per_page} registros")

            service = InstituicaoEnsinoService()
            resultado = service.get_all(page, per_page)
            resultado["data"] = instituicoesEnsinoSchema.dump(
                resultado["data"])

            logger.info("Finalizando o processamento da Listagem")
            return jsonify(resultado), 200

        except ValidationError as err:
            return {"erro": "Parâmetros de paginação inválidos", "campos": err.messages}, 400
        except DatabaseError:
            return {
                "mensagem": "Problema ao estabelecer a conexão"
            }, 500


class InstituicaoController(Resource):
    def get(self, id):
        try:
            service = InstituicaoEnsinoService()
            instituicaoEnsino = service.get_by_id(id)
            if instituicaoEnsino is None:
                return {
                    "mensagem": "Instituição de ensino não encontrada"
                }, 404
            return jsonify(instituicaoEnsinoSchema.dump(instituicaoEnsino)), 200
        except DatabaseError:
            return {
                "mensagem": "Problema ao estabelecer a conexão"
            }, 500


@instituicao_ensino_bp.post("/")
def post_instituicao():
    try:
        data = instituicaoEnsinoSchema.load(request.get_json())

        instituicao = InstituicaoEnsinoService().create(data)

        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 201

    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, 500


@instituicao_ensino_bp.put("/<int:id>")
def put_instituicao(id):
    try:
        data = instituicaoEnsinoSchema.load(request.get_json())

        instituicao = InstituicaoEnsinoService().update(id, data)

        if instituicao is None:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404

        return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 200

    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, 400

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, 500


@instituicao_ensino_bp.delete("/<int:id>")
def delete_instituicao(id):
    try:
        removida = InstituicaoEnsinoService().delete(id)

        if not removida:
            return {
                "mensagem": "Instituição de ensino não encontrada"
            }, 404

        return "", 204

    except DatabaseError:
        return {
            "mensagem": "Problema ao estabelecer a conexão"
        }, 500
