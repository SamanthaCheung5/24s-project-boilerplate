from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


# Create a blueprint for users
users = Blueprint('users', __name__)


# Get user information for a particular user
@users.route('/users/<int:userID>', methods=['GET'])
def get_id(userID):
   cursor = db.get_db().cursor()
   cursor.execute('SELECT * FROM users WHERE userID = %s', (userID,))
   row_headers = [x[0] for x in cursor.description]
   json_data =[]
   userData = cursor.fetchall()
   for row in userData:
       json_data.append(dict(zip(row_headers, row)))
   user_response = make_response(jsonify(json_data[0]))
   user_response.status_code = 200
   user_response.mimetype = 'application/json'
   return user_response


# Add a new user into the database
@users.route('/users', methods=['POST'])
def add_user():
   data = request.json
   current_app.logger.info(data)
   managerID = data['managerID']
   firstname = data['firstname']
   lastname = data['lastname']
   occupation = data['occupation']
   email = data['email']


   # Constructing the query
   query = 'insert into users (managerID, firstname, lastname, occupation, email) values ("'
   query += managerID + '", "'
   query += firstname + '", "'
   query += lastname + '", '
   query += occupation + '", '
   query += email + ')'
   current_app.logger.info(query)


    # executing and committing the insert statement
   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()
  
   return 'Successfully added new user!'


# Update user information into the database
@users.route('/users/<int:userID>', methods=['PUT'])
def update_user(userID):
   cursor = db.get_db().cursor()
   data = request.json
   current_app.logger.info(data)
   managerID = data['managerID']
   firstname = data['firstname']
   lastname = data['lastname']
   occupation = data['occupation']
   email = data['email']
  
   query = """
       UPDATE users
       SET managerID = %s, last_name = %s, first_name = %s,
           occupation = %s, email = %s
       WHERE userID = %s
   """
   try:
       cursor.execute(query, (managerID, firstname, lastname, occupation, email, userID))
       db.get_db().commit()
       return jsonify({"success": True, "message": "Customer updated successfully"}), 200
   except Exception as e:
       db.get_db().rollback()
       return jsonify({"success": False, "message": str(e)}), 500
  
# Delete user information for a particular user
@users.route('/users/<int:userID>', methods=['DELETE'])
def delete_user(userID):
   query = 'DELETE FROM users WHERE user_ID = {}'.format(userID)
   current_app.logger.info(query)
   # Executing and committing the delete statement
   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()


   return 'Instrument information deleted successfully!'


# Get market data information for a particular asset
@users.route('/marketdata/<int:assetID>', methods=['GET'])
def get_market_data(assetID):
   cursor = db.get_db().cursor()
   cursor.execute('SELECT * FROM marketdata WHERE assetID = %s', (assetID,))
   row_headers = [x[0] for x in cursor.description]
   json_data =[]
   userData = cursor.fetchall()
   for row in userData:
       json_data.append(dict(zip(row_headers, row)))
   user_response = make_response(jsonify(json_data))
   user_response.status_code = 200
   user_response.mimetype = 'application/json'
   return user_response


# Get historical data information for a particular asset
@users.route('/historicaldata/', methods=['GET'])
def get_historical_data(assetID):
   cursor = db.get_db().cursor()
   cursor.execute('SELECT * FROM historicaldata WHERE assetID = %s', (assetID,))
   row_headers = [x[0] for x in cursor.description]
   json_data =[]
   userData = cursor.fetchall()
   for row in userData:
       json_data.append(dict(zip(row_headers, row)))
   user_response = make_response(jsonify(json_data))
   user_response.status_code = 200
   user_response.mimetype = 'application/json'
   return user_response