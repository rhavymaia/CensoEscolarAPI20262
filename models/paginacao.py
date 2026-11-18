from marshmallow import Schema, fields, validate, EXCLUDE


class PaginacaoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1)
    )

    size = fields.Int(
        load_default=10,
        validate=validate.Range(min=1, max=100)
    )
