# 🏦 Simple Banking System

This project is a full-fledged **Banking System** built using **Python**, **Streamlit** for the front-end, and **MySQL** for backend storage. It allows users to create accounts, perform transactions like deposits, withdrawals, transfers, and generate reports—all through a user-friendly web interface.

---

## 📌 Features

- ✅ Account Creation with phone number verification
- 🔐 PIN-based authentication for transactions
- 💸 Deposit & Withdrawal with real-time balance updates
- 🔁 Fund Transfer with sender/receiver tracking
- 📊 Account Summary with transaction history
- 📈 Reports for top depositors and total bank balance
- 🔐 Secure transactions with MySQL logging

---

## 🛠 Tech Stack

| Technology    | Description                         |
|---------------|-------------------------------------|
| Python        | Backend business logic              |
| Streamlit     | Frontend UI framework               |
| PyMySQL       | Python-MySQL database connector     |
| MySQL         | Database to store user and transaction data |

---


---

## 🧑‍💻 Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- MySQL Server running locally
- MySQL database named `Py`
- Table structure as follows:

# sql setup

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


#  How to Run the code:

1. Make sure you have Streamlit installed:
   pip install streamlit pymysql

2. Run the app:
    streamlit run app.py

3. Access the app in your browser at:
   http://localhost:8501
