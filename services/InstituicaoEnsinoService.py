from helpers.logger import logger

from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

    def get_all(self):
        return self.instituicaoEnsinoRepository.getInstituicoes()

    def get_by_id(self, id):
        return self.instituicaoEnsinoRepository.getInstituicao(id)

    def create(self, data):
        return self.instituicaoEnsinoRepository.inserirInstituicao(data)

    def update(self, id, data):
        instituicao = self.get_by_id(id)
        if instituicao is None:
            return None
        return self.instituicaoEnsinoRepository.atualizarInstituicao(id, data)

    def delete(self, id):
        instituicao = self.get_by_id(id)
        if instituicao is None:
            return False
        return self.instituicaoEnsinoRepository.softDeleteInstituicao(id)
