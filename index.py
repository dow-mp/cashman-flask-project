from flask import Flask, jsonify, request
import json
from cashman.utils.helpers import convert_bytes_to_json, loop_to_sum

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)

# incomes = [
#     {'description': 'salary', 'amount': 5000},
#     {'description': 'uber', 'amount': 3250},
#     {'description': 'lyft', 'amount': 1570}
# ]

# @app.route('/incomes')
# def get_incomes():
#     return jsonify(incomes)

# @app.route('/incomes', methods=['POST'])
# def add_income():
#     incomes.append(request.get_json())
#     print(request.get_json())
#     return '', 201

# @app.route('/incomes', methods=['PUT'])
# def edit_income():
#     for income in incomes:
#         if request.get_json()['description'] == income['description']:
#             income['amount'] = request.get_json()['amount']
#     return incomes, 200

# @app.route('/incomes', methods=['DELETE'])
# def delete_income():
#     try:
#         incomes.remove(request.get_json())
#     except Exception as e:
#         return f"There was an error: {e}"
#     return '', 204

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('groceries', 420),
    Expense('utilities', 730)
]

@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(filter(lambda t: t.type == TransactionType.INCOME, transactions))
    # python lambdas are small anonymous functions that take any number of arguments
    # lambda arguments : expression
    # given t, does t.type == income? filter the iterable transactions when the lambda returns true (i.e. the trans type is income)
    return jsonify(incomes)

# rewrite the following functions to use the new class types
@app.route('/incomes', methods=['POST'])
def add_income():
    # incomes.append(request.get_json())
    # print(request.get_json())
    # return '', 201
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 204

@app.route('/incomes', methods=['DELETE'])
def delete_income():
    res = request.get_json()
    income_for_del = list(res.items())[0]
    for t in transactions:
        if t.description == income_for_del[1]:
            transactions.remove(t)
    return f"Successfully deleted {t}", 202
    

# @app.route('/incomes', methods=['PUT'])
# def edit_income():
#     for income in incomes:
#         if request.get_json()['description'] == income['description']:
#             income['amount'] = request.get_json()['amount']
#     return incomes, 200

# @app.route('/incomes', methods=['DELETE'])
# def delete_income():
#     try:
#         incomes.remove(request.get_json())
#     except Exception as e:
#         return f"There was an error: {e}"
#     return '', 204

@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)

@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204

@app.route('/expenses', methods=['DELETE'])
def delete_expense():
    res = request.get_json()
    expense_for_del = list(res.items())[0]
    for t in transactions:
        if t.description == expense_for_del[1]:
            transactions.remove(t)
    return f"Successfully delete {t}", 202

@app.route('/balance')
def get_bank_balance():
    incomes = convert_bytes_to_json(get_incomes)
    expenses = convert_bytes_to_json(get_expenses)

    total_income = loop_to_sum(incomes, "amount")
    total_expense = loop_to_sum(expenses, "amount")

    return jsonify(total_income + total_expense)


# TO DO: implement the update functionality
# TO DO: implemebt delete ALL functionality
# TO DO: handle errors gracefully

if __name__ == "__main__":
    app.run()