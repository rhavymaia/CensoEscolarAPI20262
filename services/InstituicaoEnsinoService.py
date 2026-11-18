import math

from helpers.logger import logger

from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

    def get_all(self, page=1, size=10):
        offset = (page - 1) * size
        itens = self.instituicaoEnsinoRepository.getInstituicoes(size, offset)
        total = self.instituicaoEnsinoRepository.countInstituicoes()
        return {
            "itens": itens,
            "page": page,
            "size": size,
            "total": total,
            "total_pages": math.ceil(total / size) if total else 0
        }

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
