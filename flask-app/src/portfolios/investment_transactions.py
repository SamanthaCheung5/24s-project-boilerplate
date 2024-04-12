########################################################
# investments_transactions blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

investments_transactions = Blueprint('investments_transactions', __name__)

# Return all transactions and their information for a particular account 
@investment_transactions.route('/<accountNum>', methods=['GET'])
def get_transactions(accountNum):
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT * FROM investment_transaction WHERE AccountNum = %s;
    """, (accountNum,))
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    cursor.close()

    json_data = [dict(zip(row_headers, result)) for result in results]
    return make_response(jsonify(json_data), 200 if results else 404)

# Update information of investment transaction in the system 
@investment_transactions.route('/<transactionID>', methods=['PUT'])
def update_transaction(transactionID):
    cursor = db.get_db().cursor()
    data = request.json
    amount = data.get('amount')
    date = data.get('date')
    type = data.get('type')

    update_query = """
        UPDATE investment_transaction
        SET Amount = %s, Date = %s, Type = %s
        WHERE TransactionID = %s;
    """
    cursor.execute(update_query, (amount, date, type, transactionID))
    db.get_db().commit()
    cursor.close()

    return jsonify({"success": True, "message": "Transaction updated successfully"}), 200
