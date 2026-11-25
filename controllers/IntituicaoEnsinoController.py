from flask import request
from psycopg2 import Error as DatabaseError
from marshmallow import ValidationError
from flask_restful import Resource

from models.instituicaoensino import InstituicaoEnsinoSchema
from models.paginacao import PaginacaoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService
from helpers.logger import logger

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)
paginacaoSchema = PaginacaoSchema()


class InstituicoesResource(Resource):
    def get(self):
        try:
            paginacao = paginacaoSchema.load(request.args)

            page = paginacao["page"]
            per_page = paginacao["per_page"]
            logger.info(
                f"Listando as Instituições de Ensino - página {page} com {per_page} registros")

            resultado = InstituicaoEnsinoService().get_all(page, per_page)
            resultado["data"] = instituicoesEnsinoSchema.dump(
                resultado["data"])

            logger.info("Finalizando o processamento da Listagem")
            return resultado, 200

        except ValidationError as err:
            return {"erro": "Parâmetros de paginação inválidos", "campos": err.messages}, 400
        except DatabaseError:
            return {"mensagem": "Problema ao estabelecer a conexão"}, 500

    def post(self):
        try:
            data = instituicaoEnsinoSchema.load(request.get_json())

            instituicao = InstituicaoEnsinoService().create(data)

            return instituicaoEnsinoSchema.dump(instituicao), 201

        except ValidationError as err:
            return {"erro": "Dados inválidos", "campos": err.messages}, 400
        except DatabaseError:
            return {"mensagem": "Problema ao estabelecer a conexão"}, 500


class InstituicaoResource(Resource):
    def get(self, id):
        try:
            instituicao = InstituicaoEnsinoService().get_by_id(id)

            if instituicao is None:
                return {"mensagem": "Instituição de ensino não encontrada"}, 404

            return instituicaoEnsinoSchema.dump(instituicao), 200

        except DatabaseError:
            return {"mensagem": "Problema ao estabelecer a conexão"}, 500

    def put(self, id):
        try:
            data = instituicaoEnsinoSchema.load(request.get_json())

            instituicao = InstituicaoEnsinoService().update(id, data)

            if instituicao is None:
                return {"mensagem": "Instituição de ensino não encontrada"}, 404

            return instituicaoEnsinoSchema.dump(instituicao), 200

        except ValidationError as err:
            return {"erro": "Dados inválidos", "campos": err.messages}, 400
        except DatabaseError:
            return {"mensagem": "Problema ao estabelecer a conexão"}, 500

    def delete(self, id):
        try:
            removida = InstituicaoEnsinoService().delete(id)

            if not removida:
                return {"mensagem": "Instituição de ensino não encontrada"}, 404

            return "", 204

        except DatabaseError:
            return {"mensagem": "Problema ao estabelecer a conexão"}, 500
