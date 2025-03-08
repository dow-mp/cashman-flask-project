import datetime as dt
import uuid

from marshmallow import Schema, fields # install with uv using uv add marshmallow
# marshmallow is a package for converting complex datatypes to and from built-in Python datatypes; we'll use it to validate, serialize, and deserialize data


class Transaction(object):
    def __init__(self, description, amount, type):
        self.description = description
        self.amount = amount
        self.created_at = dt.datetime.now()
        self.type = type
        self.id = uuid.uuid4()

    def __repr__(self):
        return f"<Transaction(name={self.description!r}, id={self.id!r})>".format(self=self)
    
# used to deserialize and serialize instances of Transaction from and to JSON objects
class TransactionSchema(Schema):
    id = fields.Str()
    description = fields.Str()
    amount = fields.Number()
    created_at = fields.Date()
    type = fields.Str()