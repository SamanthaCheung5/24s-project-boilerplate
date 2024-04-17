########################################################
# Sample accounts blueprint of endpoints
########################################################
from flask import Blueprint, request, jsonify, current_app, make_response 
import json
from src import db 


accounts = Blueprint('accounts', __name__)

# add new retirement account
@accounts.route('/income', methods=['POST'])
def add_new_income():
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    income_type = the_data['income_type']
    amount = the_data['amount']
    description = the_data['description']

    # Constructing the query
    query = 'INSERT INTO income (Type, Amount, Description) VALUES ("'
    query += income_type + '", '
    query += str(amount) + ', "'
    query += description + '")'
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

########################################################

# Return all instrumentz information for a particular Instrument_ID
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
# Get information retirement account transaction for an account
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

# Add information of a trade that took place, reflecting the transaction that occurred
@accounts.route('/trades', methods=['POST'])
def add_new_trade():
    # Collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    tradeID = the_data['TradeID']
    accountNum = the_data['Account_Number']
    date = the_data['TradeDate']
    number_of_shares = the_data['Number_of_Shares']
    price_per_share = the_data['Price_per_Share']
    total_amount = the_data['Total_Amount']
    instrumentID = the_data['InstrumentID']
    buy_or_sell = the_data['Buy_or_Sell']

    # Constructing the query for adding a new trade
    query = 'INSERT INTO trades (TradeID, Account_Number, TradeDate, Number_of_Shares, Price_per_Share, Total_Amount, InstrumentID, Buy_or_Sell) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    
    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (tradeID, accountNum, date, number_of_shares, price_per_share, total_amount, instrumentID, buy_or_sell))
    db.get_db().commit()

    return 'Trade information added successfully!'

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
