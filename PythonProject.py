# 1. Create Account
# 2. Check Balance
# 3. Deposit an Amount
# 4. Withdraw an Amount
# 0. Exit 0

import mysql.connector as m
import pandas as pd

mydatabase=m.connect(host="localhost",user="root",password="rohit@SQL",database="officemanagement")
cursor=mydatabase.cursor()

def createAccount():
    name = input("Enter your name: ")
    password = input("Enter the password: ")
    if len(password) < 8:
        print("password length should exceed 8 characters")
        password = input("Enter the password again: ")

    # balance = int(input("Enter the balance to open account with: "))
    details = (name, password)
    query1="insert into Account(Name, Password) values(%s, %s);"
    cursor.execute(query1,details)
    query_1 = "select account_number from Account where name = %s and password = %s;"
    cursor.execute(query_1,details)
    account_no=cursor.fetchall()
    mydatabase.commit()
    print("\n\nYay! Account created!\n\nYour Account Number is", account_no[0][0], "\n")
    start()

def checkBalance():
    # cursor=mydatabase.cursor()
    # balance = query
    name = input("Enter your name: ")
    accNo = int(input("Enter account number: "))######
    fetch_accounts = "select account_number from account;"
    cursor.execute(fetch_accounts)
    acc_list = cursor.fetchall()
    # print(acc_list)
    # if (accNo,) in acc_list:
    #     print(True)
    if (accNo,) in acc_list:
        password = input("Enter the password: ")
        passQry = "select password from Account where name = %s and account_number = %s;"
        cursor.execute(passQry,[name, accNo])
        orig_psswrd=cursor.fetchall()
        # print("database wala passwrd is", orig_psswrd)
        if password == orig_psswrd[0][0]:    
            query2="select balance from Account where name = %s and password = %s;"
            # details2 = [name, password]
            cursor.execute(query2,[name, password])
            balance=cursor.fetchall()
            print("\n\nBalance is: ", balance[0][0], "\n\n")
        else:
            print("Password is incorrect!")
            checkBalance()
    else:
            print("Invalid Account Number\nEnter account number again\n")
            checkBalance()
    start()

def depositAmount():
    # cursor=mydatabase.cursor()
    # balance = query
    name = input("Enter your name: ")
    acc_no = input("Enter account number: ")
    amount = int(input("Enter the Amount to Deposit: "))
    query_2="select account_number from Account where name = %s;"
    cursor.execute(query_2,[name])
    account_no=cursor.fetchall()
    query2="select balance from Account where name = %s;"
    # details2 = [name, password]
    cursor.execute(query2,[name])
    balance=cursor.fetchall()
    Acc_balance = balance[0][0] + amount
    depQuery = "insert into passbook(account_number, name, amount_credited, balance, updated_balance, time) values (%s, %s, %s, %s, %s, now())"
    cursor.execute(depQuery, [account_no[0][0] ,name, amount, balance[0][0], Acc_balance])
    query3 = "update Account set balance = %s where name = %s and account_number = %s;"
    cursor.execute(query3,[Acc_balance, name, account_no[0][0]])
    mydatabase.commit()
    print("Amount has been Successfully Credited!")
    start()


def withdrawAmount():
    # cursor=mydatabase.cursor()
    
    name = input("Enter your name: ")
    account_no = int(input("Enter account number: "))
    password = input("Enter the password: ")
    passQry = "select password from Account where name = %s;"
    cursor.execute(passQry,[name])
    orig_psswrd=cursor.fetchall()
    if password == orig_psswrd[0][0]:  #should be replaecd with account_no
        amount = int(input("Enter the Amount to Withdraw: "))
        acc_query="select account_number from Account where name = %s and password = %s;"
        cursor.execute(acc_query,[name, password])
        orig_account_no=cursor.fetchall() #should be replaced with password 
        # print(orig_account_no[0][0])
        if account_no == orig_account_no[0][0]:
            query2="select balance from Account where account_number = %s and name = %s and password = %s;"
            cursor.execute(query2,[account_no, name, password])
            balance=cursor.fetchall()
            if balance[0][0] > amount:
                Acc_balance = balance[0][0] - amount
                withQuery = "insert into passbook(account_number, name, amount_debited, balance, updated_balance, time) values (%s, %s, %s, %s, %s, now())"
                cursor.execute(withQuery, [account_no ,name, amount, balance[0][0], Acc_balance])
                query3 = "update Account set balance = %s where name = %s and password = %s;"
                cursor.execute(query3,[Acc_balance, name, password])
                mydatabase.commit()
                print("Amount successfully withdrawn!")
                start()
            else:
                print("Oopss! Balance is insufficiant!")
                start()

        else:
            print("Incorrect Account Number!")
            withdrawAmount()
    else:
        print("Incorrect Password!")
        withdrawAmount()

def printPassbook():
    name = input("Enter your name: ")
    accNo = input("Enter your account number: ")
    passQuery = "select * from passbook where name = %s and account_number = %s"
    cursor.execute(passQuery, (name, accNo))

    passInfor = cursor.fetchall()
    passInfo = pd.DataFrame(passInfor)
    if len(passInfo) != 0:

        print("\n\n")
        print(passInfo)
        print("\n\n")
    
    else:
        print("\nNo Transactions Yet\n")

    start()

def start():
    print("-----------Menu-----------")
    print("1. Create Account\n2. Check Balance\n3. Deposit an Amount\n4. Withdraw an Amount\n5. Print Passbook\n0. Exit 0\n")
    choice = int(input("Enter your Choice: "))
    if 0<=choice<=5:
        match choice:
            case 1: createAccount()
            case 2: checkBalance()
            case 3: depositAmount()
            case 4: withdrawAmount()
            case 5: printPassbook()
            case 0: exit()
            case _: print("Enter a Valid Choice!")
        
    else:
        print("\n\nInvalid choice")
        start()

start()