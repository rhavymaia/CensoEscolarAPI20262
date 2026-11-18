from marshmallow import Schema, fields, validate, EXCLUDE

PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 10
PER_PAGE_MAX = 100


class PaginacaoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    page = fields.Int(
        load_default=PAGE_DEFAULT,
        validate=validate.Range(min=1)
    )

    per_page = fields.Int(
        load_default=PER_PAGE_DEFAULT,
        validate=validate.Range(min=1, max=PER_PAGE_MAX)
    )
