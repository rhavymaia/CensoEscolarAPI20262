import math

from helpers.logger import logger

from models.paginacao import PAGE_DEFAULT, PER_PAGE_DEFAULT
from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService():
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

    def get_all(self, page=PAGE_DEFAULT, per_page=PER_PAGE_DEFAULT):
        offset = (page - 1) * per_page
        itens = self.instituicaoEnsinoRepository.getInstituicoes(per_page, offset)
        total = self.instituicaoEnsinoRepository.countInstituicoes()
        return {
            "data": itens,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": math.ceil(total / per_page) if total else 0
            }
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
