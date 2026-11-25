from flask_restful import Api

from controllers.IndexController import IndexResource, HealthResource
from controllers.IntituicaoEnsinoController import InstituicoesResource, InstituicaoResource


api = Api(prefix='/v1')
api.add_resource(IndexResource, "/")
api.add_resource(HealthResource, "/health")
api.add_resource(InstituicoesResource, "/instituicoesensino")
api.add_resource(InstituicaoResource, "/instituicoesensino/<int:id>")
