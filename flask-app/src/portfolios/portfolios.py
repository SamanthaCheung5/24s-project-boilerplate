########################################################
# portfolios blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
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
    try:
        cursor.execute(query, (investmentID, userID, portfolioType, portfolioID))
        db.get_db().commit()
        return jsonify({"success": True, "message": "Portfolio updated successfully"}), 200
    except Exception as e:
        db.get_db().rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# Create a new report for a portfolio
@portfolios.route('/reports', methods=['POST'])  
def create_report():
    the_data = request.json
    current_app.logger.info(the_data)
    portfolio_id = the_data['portfolioID']
    report_content = the_data['reportcontent']
    report_format = the_data['reportformat']
    query = """
        INSERT INTO reports (portfolioID, reportcontent, reportformat) 
        VALUES (%s, %s, %s);
    """
    conn = db.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (portfolio_id, report_content, report_format))
        conn.commit()
        report_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Failed to create report: {e}")
        return jsonify({"success": False, "message": f"Failed to create report: {e}"}), 500
    finally:
        cursor.close()

    current_app.logger.info(f"Report created with ID: {report_id}")
    return jsonify({"success": True, "reportID": report_id, "message": "Report created successfully"}), 201

# View a performance indicator by its ID
@portfolios.route('/performance_indicators/<int:indicator_ID>', methods=['GET'])
def get_performance_indicator(indicator_ID):
    cursor = db.get_db().cursor()
    query = """
        SELECT * FROM performance_indicators WHERE indicatorID = %s;
    """
    cursor.execute(query, (indicator_ID,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall() 
    cursor.close()

    json_data = []
    for row in result:
        json_data.append(dict(zip(row_headers, row)))

    if json_data:
        response = make_response(jsonify(json_data), 200)  
    else:
        response = make_response(jsonify({"error": "Performance indicator not found"}), 404)

    response.mimetype = 'application/json'
    return response

# Return all investment information for a particular InvestmentID
@portfolios.route('/investments', methods=['GET'])
def get_all_investments():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM investments')
    row_headers = [x[0] for x in cursor.description] 
    json_data = []
    all_investments = cursor.fetchall() 
    for investment in all_investments:
        json_data.append(dict(zip(row_headers, investment))) 
    cursor.close()  
    return jsonify(json_data), 200

# Add information of a particular investment reflecting the transaction that occurred
@portfolios.route('/investments', methods=['POST']) 
def add_investment():
    the_data = request.json
    current_app.logger.info(the_data)
    risk_level = the_data['risklevel']
    currency = the_data['currency']
    current_value = the_data['currentvalue']
    liquidity_ratio = the_data['liquidityratio']
    purchase_date = the_data['purchasedate']
    investment_type = the_data['investmenttype']
    purchase_price = the_data['purchaseprice']
    query = """
        INSERT INTO investments (risklevel, currency, currentvalue, liquidityratio, purchasedate, investmenttype, purchaseprice) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    current_app.logger.info(query)
    conn = db.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (risk_level, currency, current_value, liquidity_ratio, purchase_date, investment_type, purchase_price))
        conn.commit()
        response_message = jsonify({"success": True, "message": "Investment added successfully"}), 201
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Failed to add investment: {e}")
        response_message = jsonify({"success": False, "message": f"Failed to add investment: {e}"}), 500
    finally:
        cursor.close()

    return response_message

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

# Return all transactions for a particular investment
@portfolios.route('/investment_transaction/<InvestmentID>', methods=['GET']) 
def get_investment_transactions(InvestmentID):
   cursor = db.get_db().cursor()
   cursor.execute('SELECT * FROM investment_transaction WHERE InvestmentID = %s', (InvestmentID,))
   row_headers = [x[0] for x in cursor.description]
   json_data =[]
   userData = cursor.fetchall()
   for row in userData:
       json_data.append(dict(zip(row_headers, row)))
   user_response = make_response(jsonify(json_data))
   user_response.status_code = 200
   user_response.mimetype = 'application/json'
   return user_response

# Return all transactions for a particular transaction
@portfolios.route('/investment_transaction/<int:transactionID>', methods=['GET']) 
def get_transactions(transactionID):
   cursor = db.get_db().cursor()
   cursor.execute('SELECT * FROM investment_transaction WHERE transactionID = %s', (transactionID,))
   row_headers = [x[0] for x in cursor.description]
   json_data =[]
   userData = cursor.fetchall()
   for row in userData:
       json_data.append(dict(zip(row_headers, row)))
   user_response = make_response(jsonify(json_data))
   user_response.status_code = 200
   user_response.mimetype = 'application/json'
   return user_response

# Update transaction information in the system for a particular investment
@portfolios.route('/investment_transaction/<int:transactionID>', methods=['PUT'])  
def update_transaction(transactionID):
    cursor = db.get_db().cursor()
    data = request.json
    amount = data.get('amount')
    type = data.get('type')

    update_query = """
        UPDATE investment_transaction
        SET Amount = %s, Type = %s
        WHERE TransactionID = %s;
    """
    try:
        cursor.execute(update_query, (amount, type, transactionID))
        db.get_db().commit()
        return jsonify({"success": True, "message": "Transactions updated successfully"}), 200
    except Exception as e:
        db.get_db().rollback()
        return jsonify({"success": False, "message": str(e)}), 500