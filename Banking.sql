CREATE DATABASE `Bank`;

USE `Bank`;

drop table bank_accounts;
drop table transactions;


-- ✅ Updated bank_accounts with 'name' field
CREATE TABLE bank_accounts (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    account_number BIGINT NOT NULL UNIQUE,
    balance FLOAT NOT NULL DEFAULT 0.0,
    total_credited FLOAT DEFAULT 0.0,
    total_withdrawn FLOAT DEFAULT 0.0,
    pin VARCHAR(10) NOT NULL
);

-- ✅ Unchanged transactions table
CREATE TABLE transactions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    account_number BIGINT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    transaction_time DATETIME NOT NULL,
    FOREIGN KEY (account_number) REFERENCES bank_accounts(account_number) ON DELETE CASCADE
);
-- View tables
SELECT * FROM bank_accounts;
DESCRIBE bank_accounts;

SELECT * FROM transactions;
DESCRIBE transactions;
