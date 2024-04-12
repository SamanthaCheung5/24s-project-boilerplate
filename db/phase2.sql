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