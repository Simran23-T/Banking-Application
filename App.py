import pymysql
import datetime
import streamlit as st
import random

# --- DATABASE CONNECTION ---
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="********",
        database="Banking"
    )

# --- CORE FUNCTIONS ---
def generate_unique_account_number(cursor):
    while True:
        acc_num = random.randint(1000000000, 9999999999)
        cursor.execute("SELECT account_number FROM bank_accounts WHERE account_number = %s", (acc_num,))
        if not cursor.fetchone():
            return acc_num

def create_account(name, phone, password, pin):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM bank_accounts WHERE phone_number = %s", (phone,))
        if cursor.fetchone():
            return " Account already exists for this phone number."
        else:
            account_number = generate_unique_account_number(cursor)
            cursor.execute("""
                INSERT INTO bank_accounts (ID, name, phone_number, password, account_number, balance, total_credited, total_withdrawn, pin)
                VALUES (NULL, %s, %s, %s, %s, 0.0, 0.0, 0.0, %s)
            """, (name, phone, password, account_number, pin))
            db.commit()
            return f" Account created successfully!\n\nYour Account Number is: **{account_number}**"
    finally:
        cursor.close()
        db.close()

def authenticate(acc_num, pin):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bank_accounts WHERE account_number = %s AND pin = %s", (acc_num, pin))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result is not None

def deposit(acc_num, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, balance, total_credited FROM bank_accounts WHERE account_number = %s", (acc_num,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        db.close()
        return " Account not found."

    name, balance, total_credited = result
    new_balance = balance + amount
    new_total_credit = total_credited + amount

    cursor.execute("UPDATE bank_accounts SET balance = %s, total_credited = %s WHERE account_number = %s",
                   (new_balance, new_total_credit, acc_num))
    db.commit()
    log_transaction(acc_num, "deposit", amount)
    cursor.close()
    db.close()
    return f" Deposited ₹{amount} in {name} (Acc No: {acc_num}). New balance: ₹{new_balance:.2f}"


def withdraw(acc_num, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, balance, total_withdrawn FROM bank_accounts WHERE account_number = %s", (acc_num,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        db.close()
        return " Account not found."

    name, balance, total_withdrawn = result
    if balance >= amount:
        new_balance = balance - amount
        new_total_withdraw = total_withdrawn + amount
        cursor.execute("UPDATE bank_accounts SET balance = %s, total_withdrawn = %s WHERE account_number = %s",
                       (new_balance, new_total_withdraw, acc_num))
        db.commit()
        log_transaction(acc_num, "withdraw", amount)
        cursor.close()
        db.close()
        return f" Withdrew ₹{amount} from {name} (Acc No: {acc_num}). New balance: ₹{new_balance:.2f}"
    else:
        cursor.close()
        db.close()
        return " Insufficient funds."


def transfer(from_acc, to_acc, amount):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT name, balance FROM bank_accounts WHERE account_number = %s", (from_acc,))
    sender = cursor.fetchone()
    if not sender:
        cursor.close()
        db.close()
        return " Sender account not found."
    sender_name, sender_balance = sender

    cursor.execute("SELECT name, balance FROM bank_accounts WHERE account_number = %s", (to_acc,))
    receiver = cursor.fetchone()
    if not receiver:
        cursor.close()
        db.close()
        return " Recipient account not found."
    receiver_name, receiver_balance = receiver

    if sender_balance < amount:
        cursor.close()
        db.close()
        return " Insufficient funds."

    try:
        cursor.execute("UPDATE bank_accounts SET balance = balance - %s, total_withdrawn = total_withdrawn + %s WHERE account_number = %s",
                       (amount, amount, from_acc))
        cursor.execute("UPDATE bank_accounts SET balance = balance + %s, total_credited = total_credited + %s WHERE account_number = %s",
                       (amount, amount, to_acc))
        log_transaction(from_acc, "transfer_out", amount, cursor=cursor, db=db)
        log_transaction(to_acc, "transfer_in", amount, cursor=cursor, db=db)
        db.commit()
        return f" Transferred ₹{amount} from {sender_name} (Acc No: {from_acc}) to {receiver_name} (Acc No: {to_acc})."
    except Exception as e:
        db.rollback()
        return f" Error during transfer: {e}"
    finally:
        cursor.close()
        db.close()

def view_account_summary(acc_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, phone_number, account_number, balance, total_credited, total_withdrawn FROM bank_accounts WHERE account_number = %s", (acc_num,))
    account = cursor.fetchone()
    cursor.execute("SELECT transaction_type, amount, transaction_time FROM transactions WHERE account_number = %s ORDER BY transaction_time DESC", (acc_num,))
    transactions = cursor.fetchall()
    cursor.close()
    db.close()
    return account, transactions

def check_balance(acc_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (acc_num,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0] if result else None

def log_transaction(acc_num, trans_type, amount, cursor=None, db=None):
    need_close = False
    if cursor is None or db is None:
        db = connect_db()
        cursor = db.cursor()
        need_close = True
    cursor.execute("""
        INSERT INTO transactions (ID, account_number, transaction_type, amount, transaction_time)
        VALUES (NULL, %s, %s, %s, %s)
    """, (acc_num, trans_type, amount, datetime.datetime.now()))
    if need_close:
        db.commit()
        cursor.close()
        db.close()

def generate_reports():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, balance FROM bank_accounts ORDER BY balance DESC LIMIT 5")
    top_depositors = cursor.fetchall()
    cursor.execute("SELECT SUM(balance) FROM bank_accounts")
    total_balance = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return top_depositors, total_balance

# --- STREAMLIT UI ---

st.set_page_config(page_title="Banking System", layout="centered")
st.title(" Simple Banking System")

menu = [
    "Create Account", "Deposit", "Withdraw", "Transfer Money", "Check Balance", "View Account Summary", "Generate Reports"
]
choice = st.sidebar.selectbox("Choose an Option", menu)

if choice == "Create Account":
    st.header("Create Account")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    password = st.text_input("Set Password", type="password")
    pin = st.text_input("Set 4-digit PIN", type="password")
    if st.button("Create Account"):
        if not name or not phone or not password or not pin:
            st.error("❗ Please enter all fields.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("❗ PIN must be exactly 4 digits.")
        else:
            st.success(create_account(name, phone, password, pin))

elif choice == "Deposit":
    st.header("Deposit Money")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Deposit Amount", min_value=0.01)
    if st.button("Deposit"):
        if not authenticate(acc_num, pin):
            st.error(" Authentication failed.")
        else:
            st.success(deposit(acc_num, amount))

elif choice == "Withdraw":
    st.header("Withdraw Money")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Withdraw Amount", min_value=0.01)
    if st.button("Withdraw"):
        if not authenticate(acc_num, pin):
            st.error(" Authentication failed.")
        else:
            st.success(withdraw(acc_num, amount))

elif choice == "Transfer Money":
    st.header("Transfer Money")
    from_acc = st.text_input("Your Account Number")
    pin = st.text_input("Your PIN", type="password")
    to_acc = st.text_input("Recipient Account Number")
    amount = st.number_input("Amount to Transfer", min_value=0.01)
    if st.button("Transfer"):
        if not authenticate(from_acc, pin):
            st.error(" Authentication failed.")
        else:
            st.success(transfer(from_acc, to_acc, amount))

elif choice == "Check Balance":
    st.header("Check Balance")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Check Balance"):
        if not authenticate(acc_num, pin):
            st.error(" Authentication failed.")
        else:
            balance = check_balance(acc_num)
            st.success(f"Your current balance is: ₹{balance:.2f}")

elif choice == "View Account Summary":
    st.header("Account Summary")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("View Summary"):
        if not authenticate(acc_num, pin):
            st.error(" Authentication failed.")
        else:
            account, transactions = view_account_summary(acc_num)
            st.subheader("Account Details")
            st.write(f" Name: {account[0]}")
            st.write(f" Phone: {account[1]}")
            st.write(f" Account Number: {account[2]}")
            st.write(f" Balance: ₹{account[3]:.2f}")
            st.write(f" Total Credited: ₹{account[4]:.2f}")
            st.write(f" Total Withdrawn: ₹{account[5]:.2f}")
            st.subheader("Transaction History")
            if transactions:
                for t in transactions:
                    st.write(f"{t[2]} - {t[0].capitalize()} ₹{t[1]:.2f}")
            else:
                st.info("No transactions found.")

elif choice == "Generate Reports":
    st.header("Reports")
    if st.button("Generate Reports"):
        top_depositors, total_balance = generate_reports()
        st.subheader(" Top 5 Depositors")
        for depositor in top_depositors:
            st.write(f"{depositor[0]}: ₹{depositor[1]:.2f}")
        st.subheader(" Total Bank Balance")
        st.write(f"₹{total_balance:.2f}")
