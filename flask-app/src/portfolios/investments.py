########################################################
# investments blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

investments = Blueprint('investments', __name__)

# Return all investment information for a particular a {InvestmentID}
@investments.route('/<investmentID>', methods=['GET'])
def get_investment(investmentID):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM investments WHERE investmentID = %s;", (investmentID,))
    row_headers = [x[0] for x in cursor.description]  # Extract row headers
    result = cursor.fetchone()
    cursor.close()

    if result:
        json_data = dict(zip(row_headers, result))
        response = make_response(jsonify(json_data), 200)
    else:
        response = make_response(jsonify({"error": "Investment not found"}), 404)
    
    response.mimetype = 'application/json'
    return response

# Add information of a particular investment {InvestmentID} that took place, reflecting the transaction that occurred
@investments.route('/', methods=['POST'])
def add_investment():
    cursor = db.get_db().cursor()
    data = request.json
    # Extract attributes from data and create SQL insert statement
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

# Delete investment data for a particular {InvestmentID} 
@investments.route('/<investmentID>', methods=['DELETE'])
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