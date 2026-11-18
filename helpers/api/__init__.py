from flask_restful import Api

from controllers.IntituicaoEnsinoController import InstituicoesController
from helpers.application import app


api = Api(app)
api.add_resource(InstituicoesController, "/instituicoesensino")
