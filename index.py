from flask import Flask, jsonify, request
from cashman.utils.helpers import convert_bytes_to_json, loop_to_sum

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('salary', 5000),
    Expense('groceries', 420),
]

@app.route('/incomes')
def get_incomes():
    try:
        schema = IncomeSchema(many=True)
        incomes = schema.dump(filter(lambda t: t.type == TransactionType.INCOME, transactions))
        if incomes:
            return jsonify(incomes)
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/incomes', methods=['POST'])
def add_income():
    try:
        if request.get_json():
            income = IncomeSchema().load(request.get_json())
            transactions.append(income)
            return "", 204
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/incomes', methods=['DELETE'])
def delete_income():
    try:
        if request.get_json():
            print('inside try')
            res = request.get_json()
            print(res)
            income_for_del = list(res.items())[0]
            print(income_for_del)
            for t in transactions:
                print(t)
                if t.description == income_for_del[1]:
                    transactions.remove(t)
            return f"Successfully deleted {t}", 202
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/all/<type>', methods=['DELETE'])
def delete_all(type):
    try:
        transaction_type = type.upper()
        if transaction_type == 'INCOME' or transaction_type == 'EXPENSE':
            global transactions
            if transaction_type == 'INCOME' or transaction_type == 'INCOMES':
                rem_transactions = [t for t in transactions if t.type != TransactionType.INCOME]
            if transaction_type == 'EXPENSE' or transaction_type == 'EXPENSES':
                rem_transactions = [t for t in transactions if t.type != TransactionType.EXPENSE]
            transactions = rem_transactions
            return f"Successfully deleted all {transaction_type} transactions", 200
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/edit/<description>', methods=['PUT'])
def edit_transaction(description):
    try:
        if request.get_json():
            req = request.get_json()
            updates = list(req.items())
            for t in transactions:
                if t.description == description:
                    t.amount = updates[1][1]
            return f"Item {description} successfully updated.", 418
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/expenses')
def get_expenses():
    try:
        schema = ExpenseSchema(many=True)
        expenses = schema.dump(
            filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
        )
        if expenses:
            return jsonify(expenses)
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/expenses', methods=['POST'])
def add_expense():
    try:
        if request.get_json():
            expense = ExpenseSchema().load(request.get_json())
            transactions.append(expense)
            return "", 204
        else: 
            raise Exception
    except Exception as e:
        return e

@app.route('/expenses', methods=['DELETE'])
def delete_expense():
    try:
        if request.get_json():
            res = request.get_json()
            expense_for_del = list(res.items())[0]
            for t in transactions:
                if t.description == expense_for_del[1]:
                    transactions.remove(t)
            return f"Successfully delete {t}", 202
        else:
            raise Exception
    except Exception as e:
        return e

@app.route('/balance')
def get_bank_balance():
    try:
        incomes = convert_bytes_to_json(get_incomes)
        expenses = convert_bytes_to_json(get_expenses)

        if incomes and expenses:
            total_income = loop_to_sum(incomes, "amount")
            total_expense = loop_to_sum(expenses, "amount")
            return jsonify(total_income + total_expense)
        elif incomes or expenses:
            raise Exception("Cannot calculate balance without both incomes and expenses")
        else:
            raise Exception
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run()