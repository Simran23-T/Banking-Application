# 🏦 Simple Banking System

A user-friendly **Banking System** built using **Python**, **Streamlit**, and **MySQL**. This web-based application allows users to create accounts, manage transactions (deposit, withdraw, transfer), and view reports via a secure and intuitive interface.

🔗 **Live Demo:** [https://banking-application.streamlit.app/](https://banking-application.streamlit.app/)

---

## 🚀 Features

- 🔐 Account creation with phone number & PIN-based authentication
- 💰 Deposit & Withdraw with real-time balance updates
- 🔁 Fund transfer between accounts
- 📄 Account summary with full transaction history
- 📈 Reports: top depositors and total bank balance
- 🛡️ Secure transaction logging in MySQL

---

## 🛠️ Tech Stack

| Technology | Role                           |
|------------|--------------------------------|
| Python     | Backend logic                  |
| Streamlit  | Web-based front-end interface  |
| MySQL      | Relational database            |
| PyMySQL    | Python-MySQL database connector|

---

## 🧑‍💻 Installation & Setup

### ✅ Prerequisites

- Python 3.8 or higher
- MySQL Server running locally
- MySQL database named `Banking`

### 📦 Step 1: Clone the Repo

```bash
git clone https://github.com/your-username/simple-banking-system.git
cd simple-banking-system
```


Step 2: Install Dependencies

pip install streamlit pymysql



 Step 3: MySQL Setup
Open MySQL and execute the contents of Banking.sql



Step 4: Run the App Locally
streamlit run app.py
