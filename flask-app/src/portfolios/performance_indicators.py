########################################################
# performance_indicators blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

performance_indicators = Blueprint('performance_indicators', __name__)

# View a client’s portfolio indicator
@performance_indicators.route('/<indicator_ID>', methods=['GET'])
def get_performance_indicator(indicator_ID):
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT * FROM performance_indicators WHERE indicatorID = %s;
    """, (indicator_ID,))
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    result = cursor.fetchone()
    cursor.close()

    if result:
        json_data = dict(zip(row_headers, result))
        response = make_response(jsonify(json_data), 200)
    else:
        response = make_response(jsonify({"error": "Performance indicator not found"}), 404)
    
    response.mimetype = 'application/json'
    return response