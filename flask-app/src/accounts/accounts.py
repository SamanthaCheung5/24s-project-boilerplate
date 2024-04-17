########################################################
# Sample accounts blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, current_app, make_response 
import json
from src import db 


accounts = Blueprint('accounts', __name__)

# add a new source of income
@accounts.route('/income', methods=['POST'])
def add_new_income():
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    Type = the_data['Type']
    Amount = the_data['Amount']
    Description = the_data['Description']

    # Constructing the query
    query = 'INSERT INTO income (Type, Amount, Description) VALUES ("'
    query += Type + '", '
    query += str(Amount) + ', "'
    query += Description + '")'
    current_app.logger.info(query)

    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success!'

########################################################
# Get info for income
@accounts.route('/income', methods=['GET'])
def get_all_income_info():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM income')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))

    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

########################################################
# Update instrument information for a specific instrumentID (PUT request)
@accounts.route('/instruments/<int:instrumentID>', methods=['PUT'])
def update_instrument(instrumentID):
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    accountNum = the_data['accountNum']
    quotes = the_data['quotes']
    instrument_type = the_data['type']

    # Constructing the query for updating instrument information
    query = 'UPDATE instruments SET accountNum = {}, quotes = {}, type = "{}" WHERE instrument_ID = {}'.format(
        accountNum, quotes, instrument_type, instrumentID)
    current_app.logger.info(query)

    # Executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Instrument information updated successfully!'

########################################################

# Return all instruments information for a particular Instrument_ID
@accounts.route('/instruments', methods=['GET'])
def get_all_instruments():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM instruments')
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    all_instruments = cursor.fetchall()  
    for instrument in all_instruments:
        json_data.append(dict(zip(row_headers, instrument)))  
    cursor.close()  # Close the cursor
    return jsonify(json_data), 200

########################################################

# Delete instrument information for a specific instrumentID (DELETE request)
@accounts.route('/instruments/<int:instrumentID>', methods=['DELETE'])
def delete_instrument(instrumentID):
    # Constructing the query for deleting instrument information
    query = 'DELETE FROM instruments WHERE instrument_ID = {}'.format(instrumentID)
    current_app.logger.info(query)

    # Executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Instrument information deleted successfully!'

if __name__ == '__main__':
    app.run(debug=True)

########################################################
# Get all trade information for a particular account
@accounts.route('/trades/<int:accountNum>', methods=['GET'])
def get_trades(accountNum):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM trades WHERE accountNum = %s', (accountNum,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))
    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

########################################################
# Get a list of all accountID numbers
@accounts.route('/accounts', methods=['GET'])
def get_account_ids():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT accountNum FROM trades')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))

    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

########################################################
# Get information retirement account for an account
@accounts.route('/retirement_account/<int:account_num>', methods=['GET'])
def get_retirement_account(account_num):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM retirement_account WHERE account_num = %s', (account_num,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))

    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

# Get a list of all accountNum for retirement acc
@accounts.route('/retirement_account', methods=['GET'])
def get_account_nums():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT account_num FROM retirement_account')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))

    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

# Get trade information headers
@accounts.route('/trades/', methods=['GET'])
def get_trade_header():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM trades')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))

    user_response = make_response(jsonify(json_data[0]))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

# Return all account information for a particular user
@accounts.route('/accounts/<int:userID>', methods=['GET'])
def get_accounts(userID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM accounts WHERE userID = %s', (userID,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    userData = cursor.fetchall()
    for row in userData:
        json_data.append(dict(zip(row_headers, row)))
    user_response = make_response(jsonify(json_data))
    user_response.status_code = 200
    user_response.mimetype = 'application/json'
    return user_response

if __name__ == '__main__':
    app.run(debug=True)
