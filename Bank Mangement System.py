"""
-- SQL Commands to create and set up the database

CREATE DATABASE bankmanagement;
USE bankmanagement;

CREATE TABLE user (
    UserId BIGINT PRIMARY KEY, 
    password VARCHAR(20) NOT NULL,
    accno INT
);

CREATE TABLE accdetails (
    accno INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(20), 
    phno BIGINT, 
    balance FLOAT(15,2)
);

INSERT INTO user (UserId, password, accno) VALUES
    (123445, 'hello', 1456754321),
    (123446, 'qwerty', 1456754322);

INSERT INTO accdetails (accno, name, phno, balance) VALUES 
    (1456754321, 'Aastha', 9774508280, 45347.21),
    (1456754322, 'Belkin', 8881549062, 18923.78);
"""




import pymysql
import matplotlib.pyplot as plt
import numpy as np

def abt():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()

    print('\nAbout EPSILON Bank')
    print('In today\'s growing economic world, it is very important to ensure that we are financially stable and that our finances are maintained properly.')
    print('Epsilon Bank serves this purpose.')
    print("We at Epsilon Bank make sure that customer's satisfaction is our utmost priority.")
    print('Epsilon Bank provides you the safest and fastest means of transactions.')
    print('The tremendous growth of users over the past 7 years demonstrates our credibility.')

    years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024])
    newacc = np.array([8049, 23478, 33676, 53218, 60234, 75000, 82000])
    plt.bar(years, newacc, color=['mediumpurple'])
    plt.title('Number of New Accounts Opened in the past 7 years')
    plt.xlabel('Year')
    plt.ylabel('Number of Accounts Opened')
    plt.show()

    conn.close()

def withdrawal():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()
    accno = input('\n\nEnter your account number :: ')
    w = float(input('Enter amount to be withdrawn :: '))

    # Use parameterized query
    a.execute('SELECT balance FROM accdetails WHERE accno=%s', (accno,))
    x = a.fetchone()

    if x is None:
        print('\n\nInvalid Account Number')
    else:
        balance = x[0]
        if balance >= w:
            g = int(input('Are you sure that you want to withdraw ' + str(w) + ' from your account? [No=0/Yes=1]'))
            if g == 1:
                new_balance = balance - w
                # Use parameterized query
                a.execute('UPDATE accdetails SET balance=%s WHERE accno=%s', (new_balance, accno))
                print('\n\nYour transaction was successful \n\nYour updated balance is ::', new_balance)
        else:
            print('Insufficient Balance. Please check the amount entered')

    conn.commit()
    conn.close()

def deposit():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()
    accno = input('\n\nEnter your account number :: ')
    d = float(input('\n\nEnter Deposit amount ::'))

    # Use parameterized query
    a.execute('SELECT balance FROM accdetails WHERE accno=%s', (accno,))
    x = a.fetchone()

    if x is None:
        print('\n\nInvalid Account Number')
    else:
        balance = x[0]
        g = int(input('Are you sure that you want to deposit ' + str(d) + ' to your account? [No=0/Yes=1]'))
        if g == 1:
            new_balance = balance + d
            # Use parameterized query
            a.execute('UPDATE accdetails SET balance=%s WHERE accno=%s', (new_balance, accno))
            print('\n\nYour transaction was successful \n\nYour updated balance is ::', new_balance)

    conn.commit()
    conn.close()

def details():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()
    r = int(input('\nEnter account number ::'))
    a.execute('SELECT * FROM accdetails WHERE accno=%s', (r,))
    data = a.fetchone()

    if data is None:
        print('\n\nInvalid Account Number')
    else:
        print('\n\n::::Account details::::')
        print('\nAccount Number=', data[0])
        print('Name=', data[1])
        print('Phone Number=', data[2])
        print('Available Balance', data[3])
        print('\n\n')

    conn.close()

def closeacc():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()
    accno = input('\n\nEnter your account number :: ')
    a.execute('SELECT * FROM user WHERE accno=%s', (accno,))
    x = a.fetchone()

    if x is None:
        print('\n\nInvalid Account Number')
    else:
        pwd = input('Enter Password ::')
        pwdcheck = checkpassword(accno)
        if pwdcheck == pwd:
            p = int(input("Are you sure you want to delete your account? [No=0/Yes=1]"))
            if p == 1:
                a.execute('DELETE FROM accdetails WHERE accno=%s', (accno,))
                a.execute('DELETE FROM user WHERE accno=%s', (accno,))
                print('\n\nAccount Deleted')
        else:
            print('\n\nIncorrect Password')

    conn.commit()
    conn.close()

def NewAcc():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
    a = conn.cursor()

    name = input('Enter your name:')
    phoneno = int(input('Enter your phone number:'))
    balance = float(input('Enter Balance:'))

    # Use parameterized query
    a.execute('INSERT INTO accdetails (name, phno, balance) VALUES (%s, %s, %s)', (name, phoneno, balance))

    print('Account created ')
    # Use parameterized query
    a.execute('SELECT accno FROM accdetails WHERE phno=%s', (phoneno,))
    t = a.fetchone()[0]

    user = int(input('Enter UserId ::'))
    s = 'select * from user where UserId=%s'
    a.execute(s, (user,))
    r = a.rowcount
    while r != 0:
        print('This UserId already exists, Please enter a DIFFERENT UserId')
        user = int(input('Enter UserId ::'))
        a.execute(s, (user,))
        r = a.rowcount

    pwd = input('Enter Password ::')
    a.execute('INSERT INTO user (UserId, password, accno) VALUES (%s, %s, %s)', (user, pwd, t))
    print('\n\nThis is your Account Number :', t)

    conn.commit()
    conn.close()

def checkpassword(accno):
    # Implement this function to return the correct password for the given account number
    pass

print('::::: WELCOME TO EPSILON BANK :::::')

while True:
    print('\nPlease select your choice ')
    ad = int(input('''1. About Bank
2. Login
3. Create New Account
\nEnter your choice ::'''))

    if ad == 1:
        abt()

    elif ad == 2:
        user = input('\nEnter UserID ::')
        pwd = input('Enter password ::')
        print('\n')

        conn = pymysql.connect(host='localhost', user='root', password='root', database='bankmanagement')
        a = conn.cursor()

        s = 'SELECT * FROM user WHERE UserId=%s'
        a.execute(s, (user,))
        r = a.rowcount
        if r == 0:
            print('Invalid username')
        else:
            s = 'SELECT * FROM user WHERE password=%s'
            a.execute(s, (pwd,))
            r = a.rowcount
            if r == 0:
                print('Invalid Password')
            else:
                while True:
                    print('Select your choice')
                    print('1. Withdrawal')
                    print('2. Deposit')
                    print('3. Display details')
                    print('4. Close account')
                    print('5. Logout')

                    ch = int(input('\nEnter your choice ::'))

                    if ch == 1:
                        withdrawal()
                    elif ch == 2:
                        deposit()
                    elif ch == 3:
                        details()
                    elif ch == 4:
                        closeacc()
                    elif ch == 5:
                        break

        conn.close()

    elif ad == 3:
        NewAcc()

    else:
        print('\nPlease Enter a Valid Choice')
