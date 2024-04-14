########################################################
# portfolios blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

portfolios = Blueprint('portfolios', __name__)

# Update existing portfolio data
@portfolios.route('/portfolios/<int:portfolioID>', methods=['PUT'])
def update_portfolio(portfolioID):
    cursor = db.get_db().cursor()
    data = request.json
    investmentID = data.get('investmentID')
    userID = data.get('userID')
    portfolioType = data.get('portfolioType')
    
    query = """
        UPDATE portfolios
        SET investmentID = %s, userID = %s, portfolioType = %s
        WHERE portfolioID = %s
    """
    cursor.execute(query, (investmentID, userID, portfolioType, portfolioID))
    db.get_db().commit()
    
    response = jsonify({"success": True, "message": "Portfolio updated successfully"}), 200
    
    cursor.close()
    return response

# Create a new report for a portfolio
@portfolios.route('/reports', methods=['POST'])  
def create_report():
    cursor = db.get_db().cursor()
    data = request.json
    portfolioID = data.get('portfolioID')
    reportcontent = data.get('reportcontent')
    reportformat = data.get('reportformat')
    
    query = """
        INSERT INTO reports (portfolioID, reportcontent, reportformat) 
        VALUES (%s, %s, %s);
    """
    cursor.execute(query, (portfolioID, reportcontent, reportformat))
    db.get_db().commit()
    reportID = cursor.lastrowid
    cursor.close()
    return jsonify({"success": True, "reportID": reportID, "message": "Report created successfully"}), 201

# View a performance indicator by its ID
@portfolios.route('/performance_indicators/<int:indicator_ID>', methods=['GET'])
def get_performance_indicator(indicator_ID):
    cursor = db.get_db().cursor()
    query = """
        SELECT * FROM performance_indicators WHERE indicatorID = %s;
    """
    cursor.execute(query, (indicator_ID,))
    row_headers = [x[0] for x in cursor.description]  
    result = cursor.fetchone()
    cursor.close()

    if result:
        json_data = dict(zip(row_headers, result))
        response = make_response(jsonify(json_data), 200)
    else:
        response = make_response(jsonify({"error": "Performance indicator not found"}), 404)
    
    response.mimetype = 'application/json'
    return response

# Return all investment information for a particular InvestmentID
@portfolios.route('/investments/<int:investmentID>', methods=['GET'])
def get_investment(investmentID):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM investments WHERE investmentID = %s;", (investmentID,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    cursor.close()

    if result:
        json_data = dict(zip(row_headers, result))
        response = make_response(jsonify(json_data), 200)
    else:
        response = make_response(jsonify({"error": "Investment not found"}), 404)
    
    response.mimetype = 'application/json'
    return response

# Add information of a particular investment reflecting the transaction that occurred
@portfolios.route('/investments', methods=['POST']) 
def add_investment():
    cursor = db.get_db().cursor()
    data = request.json
    query = """
        INSERT INTO investments (risklevel, currency, currentvalue, liquidityratio, purchasedate, investmenttype, purchaseprice)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (data['risklevel'], data['currency'], data['currentvalue'], 
                           data['liquidityratio'], data['purchasedate'], data['investmenttype'], 
                           data['purchaseprice']))
    db.get_db().commit()
    cursor.close()

    return jsonify({"success": True, "message": "Investment added successfully"}), 201

# Delete investment data for a particular InvestmentID
@portfolios.route('/investments/<int:investmentID>', methods=['DELETE'])
def delete_investment(investmentID):
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM investments WHERE investmentID = %s;", (investmentID,))
    db.get_db().commit()
    deleted_rows = cursor.rowcount
    cursor.close()

    if deleted_rows:
        return jsonify({"success": True, "message": "Investment deleted successfully"}), 200
    else:
        return jsonify({"error": "Investment not found"}), 404

# Return all transactions for a particular account number
@portfolios.route('/investment_transactions/<accountNum>', methods=['GET']) 
def get_transactions(accountNum):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM investment_transaction WHERE AccountNum = %s;", (accountNum,))
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    cursor.close()

    json_data = [dict(zip(row_headers, result)) for result in results]
    return make_response(jsonify(json_data), 200 if results else 404)

# Update transaction information in the system
@portfolios.route('/investment_transactions/<int:transactionID>', methods=['PUT'])  
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
