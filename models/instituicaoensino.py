from marshmallow import Schema, fields, validate


class InstituicaoEnsino():
    def __init__(
        self,
        no_entidade,
        co_entidade,
        no_uf,
        sg_uf,
        co_uf,
        no_municipio,
        co_municipio,
        nu_ano_censo,
        qt_mat_bas,
        qt_mat_inf,
        qt_mat_fund,
        qt_mat_med,
        qt_mat_prof,
        qt_mat_eja,
        qt_mat_esp
    ):
        self.no_entidade = no_entidade
        self.co_entidade = co_entidade
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_uf = co_uf
        self.no_municipio = no_municipio
        self.co_municipio = co_municipio
        self.nu_ano_censo = nu_ano_censo
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_med = qt_mat_med
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp

    def toDict(self):
        return {"no_entidade": self.no_entidade, "co_entidade": self.co_entidade, "qt_mat_bas": self.qt_mat_bas}


class InstituicaoEnsinoSchema(Schema):

    id = fields.Int(dump_only=True)

    no_entidade = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    co_entidade = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    no_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    sg_uf = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2)
    )

    co_uf = fields.Int(
        required=True
    )

    no_municipio = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    co_municipio = fields.Int(
        required=True
    )

    nu_ano_censo = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_bas = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_inf = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_fund = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_med = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_prof = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_eja = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    qt_mat_esp = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    created = fields.DateTime(
        dump_only=True
    )
