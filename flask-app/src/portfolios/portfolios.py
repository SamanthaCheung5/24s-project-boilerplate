########################################################
# portfolios blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

portfolios = Blueprint('portfolios', __name__)

# Update existing portfolio data
@portfolios.route('/<int:portfolioID>', methods=['PUT'])
def update_portfolio(portfolioID):
    cursor = db.get_db().cursor()
    data = request.json
    investmentID = data.get('investmentID')
    userID = data.get('userID')
    portfolioType = data.get('portfolioType')
    
    # Update query to match portfolio attributes
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