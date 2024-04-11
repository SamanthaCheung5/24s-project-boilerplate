-- Create Investment Portfolio Database
CREATE DATABASE IF NOT EXISTS investment_portfolio;

-- Use Investment Portfolio Database
USE investment_portfolio;

-- Create managers table
CREATE TABLE IF NOT EXISTS managers(
    managerID INT PRIMARY KEY,
    email VARCHAR(30),
    accountcreation DATETIME DEFAULT CURRENT_TIMESTAMP,
    phone VARCHAR(15),
    name VARCHAR(60),
    lastlogindate DATETIME DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABlE IF NOT EXISTS users(
    userID INT AUTO_INCREMENT PRIMARY KEY,
    managerID INT,
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    occupation VARCHAR(30),
    email VARCHAR(30),
    accountcreation DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users FOREIGN KEY (managerID)
        REFERENCES managers(managerID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create marketdata table
CREATE TABLE IF NOT EXISTS marketdata(
    assetID INT PRIMARY KEY,
    currentprice FLOAT,
    highprice FLOAT,
    lowprice FLOAT,
    datasource VARCHAR(50)
);

-- Create historicaldata table
CREATE TABLE IF NOT EXISTS historicaldata(
    assetID INT,
    datechanged DATETIME DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,
    price FLOAT,
    PRIMARY KEY(assetID, datechanged),
    CONSTRAINT fk_historicaldata FOREIGN KEY (assetID)
        REFERENCES marketdata(assetID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create userviewhistory table
CREATE TABLE IF NOT EXISTS userviewhistory(
    assetID INT,
    userID INT,
    PRIMARY KEY(assetID, userID),
    CONSTRAINT fk_userviewhistory1 FOREIGN KEY (assetID)
        REFERENCES marketdata(assetID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_userviewhistory2 FOREIGN KEY (userID)
        REFERENCES users(userID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts(
    accountNum INT PRIMARY KEY,
    userID INT,
    cashbalance FLOAT,
    investmentvalue FLOAT,
    totalvalue FLOAT,
    CONSTRAINT fk_04 FOREIGN KEY (userID)
        REFERENCES users(userID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create investments table
CREATE TABLE IF NOT EXISTS investments (
    investmentID INT AUTO_INCREMENT PRIMARY KEY,
    risklevel VARCHAR(50),
    currency VARCHAR(3),
    currentvalue DECIMAL(10,2),
    liquidityratio VARCHAR(50),
    purchasedate DATETIME DEFAULT CURRENT_TIMESTAMP,
    investmenttype VARCHAR(50),
    purchaseprice DECIMAL(10,2)
);

-- Create portfolios table
CREATE TABLE IF NOT EXISTS portfolios (
    portfolioID INT AUTO_INCREMENT PRIMARY KEY,
    investmentID INT,
    userID INT,
    portfolioType VARCHAR(50),
    creationdate DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_portfolios_investments FOREIGN KEY (InvestmentID)
       REFERENCES investments(investmentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_portfolios_clients FOREIGN KEY (userID)
       REFERENCES users(userID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);

-- Create performance_indicators table
CREATE TABLE IF NOT EXISTS performance_indicators (
    indicatorID INT AUTO_INCREMENT PRIMARY KEY,
    portfolioID INT NOT NULL,
    datemeasured DATETIME DEFAULT CURRENT_TIMESTAMP,
    risklevel VARCHAR(50),
    totalvalue DECIMAL(10,2),
    growthpercentage DECIMAL(5,2),
    CONSTRAINT fk_performanceindicators_portfolios FOREIGN KEY (PortfolioID)
       REFERENCES portfolios(portfolioID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);

-- Create reports table
CREATE TABLE IF NOT EXISTS reports (
    reportID INT AUTO_INCREMENT PRIMARY KEY,
    portfolioID INT,
    generationdate DATETIME DEFAULT CURRENT_TIMESTAMP,
    reportcontent TEXT,
    reportformat VARCHAR(50),
    CONSTRAINT fk_reports_portfolios FOREIGN KEY (PortfolioID)
       REFERENCES portfolios(portfolioID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);

-- Create retirement_account table
CREATE TABLE IF NOT EXISTS retirement_account
(
   account_num INTEGER,
   userID INTEGER,
   account_type varchar(50),
   cash_balance decimal,
   contribution_limit decimal,
   total_limit decimal,
   PRIMARY KEY (account_num),
   CONSTRAINT fk_retirement_account
   FOREIGN KEY (userID) REFERENCES users(userID) ON UPDATE CASCADE ON DELETE CASCADE
);


-- Create retirement_transaction table
CREATE TABLE IF NOT EXISTS retirement_transaction
(
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   account_num INTEGER,
   transaction_type varchar(50),
   amount FLOAT,
   PRIMARY KEY (timestamp, account_num),
   CONSTRAINT fk_retirement_transaction
   FOREIGN KEY (account_num) REFERENCES retirement_account(account_num)
       ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create Income Table
CREATE TABLE IF NOT EXISTS income(
   IncomeID INTEGER AUTO_INCREMENT PRIMARY KEY,
   Date DATETIME DEFAULT CURRENT_TIMESTAMP,
   Type VARCHAR(10),
   Amount INTEGER,
   Description VARCHAR(250)
);


-- Create Investment Transactions Table
CREATE TABLE IF NOT EXISTS investment_transaction(
   TransactionID INTEGER AUTO_INCREMENT PRIMARY KEY,
   IncomeID INTEGER,
   InvestmentID INTEGER,
   Amount INTEGER,
   Date DATETIME DEFAULT CURRENT_TIMESTAMP,
   Type VARCHAR(50),
   CONSTRAINT fk_investment_transaction1 FOREIGN KEY (InvestmentID)
       REFERENCES investments(InvestmentID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_investment_transaction2 FOREIGN KEY (IncomeID)
       REFERENCES income(IncomeID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);

# Create table for instruments
CREATE TABLE IF NOT EXISTS instruments (
   instrument_ID INTEGER,
   accountNum INTEGER,
   quotes decimal,
   type varchar(50),
   PRIMARY KEY (instrument_ID),
   CONSTRAINT fk_instruments
   FOREIGN KEY (accountNum) REFERENCES accounts(accountNum)
       ON UPDATE CASCADE ON DELETE CASCADE
);

# Create table for trades
CREATE TABLE IF NOT EXISTS trades (
   tradeID INTEGER,
   accountNum INTEGER,
   date DATE,
   number_of_shares INTEGER,
   price_per_share decimal,
   total_amount decimal,
   instrumentID INTEGER,
   buy_or_sell BOOLEAN,
   PRIMARY KEY (tradeID),
   CONSTRAINT fk_trades1
   FOREIGN KEY (accountNum) REFERENCES accounts(accountNum)
       ON UPDATE CASCADE ON DELETE CASCADE,
   CONSTRAINT fk_trades2
   FOREIGN KEY (instrumentID) REFERENCES instruments(instrument_ID)
       ON UPDATE CASCADE ON DELETE CASCADE
);

-- Insert into managers table
INSERT INTO managers (managerID, email, phone, name)
VALUES (1, 'debrawilson@deloitte.com', '123-456-7890', 'Debra Wilson'),
       (2, 'alexreynolds@captrust.com', '987-654-3210', 'Alex Reynolds');

-- Insert into users table
INSERT INTO users (managerID, firstname, lastname, occupation, email)
VALUES (NULL, 'Ethan', 'Thompson', 'Entrepreneur', 'ethanthompson@gmail.com'),
       (NULL, 'Randall', 'Smith', 'Retiree', 'randallsmith@gmail.com'),
       (1, 'Megan', 'Jirakulaporn', 'Student', 'jira.m@northeastern.edu'),
       (2, 'Alex', 'Choi', 'Artist', 'choi.alex@northeastern.edu');

-- Insert into marketdata table
INSERT INTO marketdata (assetID, currentprice, highprice, lowprice, datasource)
VALUES (1, 100.50, 105.75, 98.25, 'Yahoo Finance'),
       (2, 50.25, 55.30, 48.90, 'Vanguard');

-- Insert into historicaldata table
INSERT INTO historicaldata (assetID, price)
VALUES (1, 98.75),
       (2, 52.10);

-- Insert into userviewhistory table
INSERT INTO userviewhistory (assetID, userID)
VALUES (1, 1),
       (2, 2);

-- Insert into accounts table
INSERT INTO accounts (accountNum, userID, cashbalance, investmentvalue, totalvalue)
VALUES (1, 1, 5000.00, 10000.00, 15000.00),
       (2, 2, 7500.00, 7500.00, 15000.00);

-- Insert into investments table
INSERT INTO investments (risklevel, currency, currentvalue, liquidityratio, investmenttype, purchaseprice)
VALUES ('High', 'USD', 15000.00, 'Low', 'Stocks', 5000.00),
       ('Medium', 'USD', 10000.00, 'Medium', 'Bonds', 7500.00);

-- Insert into portfolios table
INSERT INTO portfolios (investmentID, userID, portfolioType)
VALUES (1, 1, 'Aggressive'),
       (2, 2, 'Balanced');

-- Insert into performance_indicators table
INSERT INTO performance_indicators (portfolioID, risklevel, totalvalue, growthpercentage)
VALUES (1, 'High', 15000.00, 5.0),
       (2, 'Medium', 15000.00, 2.5);

-- Insert into reports table
INSERT INTO reports (portfolioID, reportcontent, reportformat)
VALUES (1, 'Aggressive portfolio performance report', 'PDF'),
       (2, 'Balanced portfolio performance report', 'PDF');

-- Insert into retirement_account table
INSERT INTO retirement_account (account_num, userID, account_type, cash_balance, contribution_limit, total_limit)
VALUES (1, 1, '401(k)', 10000.00, 20000.00, 50000.00),
       (2, 2, 'IRA', 15000.00, 25000.00, 60000.00);

-- Insert into retirement_transaction table
INSERT INTO retirement_transaction (account_num, transaction_type)
VALUES (1, 'Contribution'),
       (2, 'Withdrawal');

-- Insert into income table
INSERT INTO income (Type, Amount, Description)
VALUES ('Salary', 5000, 'Monthly salary for April'),
       ('Dividend', 250, 'Stock dividend payout');

-- Insert into investment_transaction table
INSERT INTO investment_transaction (IncomeID, InvestmentID, Amount, Type)
VALUES (1, 1, 5000, 'Purchase'),
       (2, 1, 250, 'Reinvestment');

-- Insert into instruments table
INSERT INTO instruments (instrument_ID, accountNum, quotes, type)
VALUES (1, 1, 150.00, 'Stock'),
       (2, 2, 75.50, 'Bond');

-- Insert into trades table
INSERT INTO trades (tradeID, accountNum, date, number_of_shares, price_per_share, total_amount, instrumentID)
VALUES (1, 1, '2024-04-01', 50, 100.00, 5000.00, 1),
       (2, 2, '2024-04-02', 100, 75.50, 7550.00, 2);








