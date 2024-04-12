########################################################
# reports blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db

reports = Blueprint('reports', __name__)

#Create a new {reportID} for a client
@reports.route('/', methods=['POST'])
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