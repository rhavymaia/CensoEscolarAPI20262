from flask_restful import Resource


class IndexResource(Resource):
    def get(self):
        return {"versao": "0.0.1"}, 200


class HealthResource(Resource):
    def get(self):
        return {"health": "ok"}, 200
