from marshmallow import post_load

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Income(Transaction):
    def __init__(self, description, amount):
        super(Income, self).__init__(description, amount, TransactionType.INCOME)

    def __repr__(self):
        return '<Income(name={self.description!r})>'.format(self=self)
    

class IncomeSchema(TransactionSchema):
    @post_load
    def make_income(self, data, **kwargs):
        return Income(**data)
    

    # incomes = schema.dump(filter(lambda t: t.type == TransactionType.INCOME, transactions))
    # python lambdas are small anonymous functions that take any number of arguments
    # lambda arguments : expression
    # given t, does t.type == income? filter the iterable transactions when the lambda returns true (i.e. the trans type is income)