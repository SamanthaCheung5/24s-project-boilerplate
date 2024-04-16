########################################################
# Sample accounts blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, current_app, make_response 
import json
from src import db


accounts = Blueprint('accounts', __name__)

# add a new retirement transaction 
@accounts.route('/retirement_transaction/<int:account_num>', methods=['POST'])
def add_new_retirement_transaction(account_num):

    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    transaction_type = the_data['transaction_type']
    amount = the_data['amount']

    # Constructing the query
    query = 'INSERT INTO retirement_transaction (account_num, transaction_type, amount) VALUES ('
    query += str(account_num) + ', "'
    query += transaction_type + '", '
    query += str(amount) + ')'
    current_app.logger.info(query)

    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success!'

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

# Get instrument information for a specific instrumentID (GET)
@accounts.route('/instruments', methods=['GET'])
def get_all_instruments():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM instruments')
    row_headers = [x[0] for x in cursor.description]  # Extract the column headers
    json_data = []
    all_instruments = cursor.fetchall()  # Fetch all rows from the database
    for instruments in all_instruments:
        json_data.append(dict(zip(row_headers, instruments)))  # Create a dictionary for each investment row
    cursor.close()  # Close the cursor
    return jsonify(json_data), 200
########################################################

# Delete instrument information for a specific instrumentID (DELETE request)
@accounts.route('/instruments/<int:instrument_ID>', methods=['DELETE'])
def delete_instruments(instrument_ID):
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM instruments WHERE instrument_ID = %s;", (instrument_ID,))
    db.get_db().commit()
    deleted_rows = cursor.rowcount
    cursor.close()

    if deleted_rows:
        return jsonify({"success": True, "message": "Instrument deleted successfully"}), 200
    else:
        return jsonify({"error": "Instrument not found"}), 404

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

# Add information of a trade that took place, reflecting the transaction that occurred
@accounts.route('/trades', methods=['POST'])
def add_new_trade():
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    accountNum = the_data['accountNum']
    date = the_data['date']
    number_of_shares = the_data['number_of_shares']
    price_per_share = the_data['price_per_share']
    total_amount = the_data['total_amount']
    instrumentID = the_data['instrumentID']
    buy_or_sell = the_data['buy_or_sell']

    # Constructing the query for adding a new trade
    query = 'INSERT INTO trades (accountNum, date, number_of_shares, price_per_share, total_amount, instrumentID, buy_or_sell) VALUES ({}, "{}", {}, {}, {}, {}, {})'.format(
        accountNum, date, number_of_shares, price_per_share, total_amount, instrumentID, buy_or_sell)
    current_app.logger.info(query)

    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Trade information added successfully!'

########################################################

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
