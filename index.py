from flask import Flask, jsonify, request
from cashman.utils.helpers import convert_bytes_to_json, loop_to_sum

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('salary', 5000),
    Income('stock', 200),
    Income('uber', 5000),
    Income('deliveries', 200),
    Expense('groceries', 420),
    Expense('utilities', 730),
    Expense('gas', 420),
    Expense('rent', 1730)
]

@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(filter(lambda t: t.type == TransactionType.INCOME, transactions))
    return jsonify(incomes)

@app.route('/incomes', methods=['POST'])
def add_income():
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

@app.route('/all/<type>', methods=['DELETE'])
def delete_all(type):
    transaction_type = type.upper()
    global transactions
    if transaction_type == 'INCOME' or transaction_type == 'INCOMES':
        rem_transactions = [t for t in transactions if t.type != TransactionType.INCOME]
    if transaction_type == 'EXPENSE' or transaction_type == 'EXPENSES':
        rem_transactions = [t for t in transactions if t.type != TransactionType.EXPENSE]
    transactions = rem_transactions
    return f"Successfully deleted all {transaction_type} transactions", 200

@app.route('/edit/<description>', methods=['PUT'])
def edit_transaction(description):
    req = request.get_json()
    updates = list(req.items())
    for t in transactions:
        if t.description == description:
            t.amount = updates[1][1]
    return f"Item {description} successfully updated.", 418

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


if __name__ == "__main__":
    app.run()