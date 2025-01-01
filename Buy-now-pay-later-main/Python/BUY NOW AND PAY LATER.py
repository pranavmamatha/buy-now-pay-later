print("""
░█████╗░███████╗██╗░░██╗░█████╗░██████╗░░█████╗░  ░██████╗████████╗░█████╗░██████╗░███████╗
██╔══██╗╚════██║██║░░██║██╔══██╗██╔══██╗██╔══██╗  ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
███████║░░███╔═╝███████║███████║██████╔╝███████║  ╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░
██╔══██║██╔══╝░░██╔══██║██╔══██║██╔══██╗██╔══██║  ░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░
██║░░██║███████╗██║░░██║██║░░██║██║░░██║██║░░██║  ██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗
╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝                                                                                       
""")
print("""
█████████████████████████████████████████████████████████████████████████████████████████████████
█▄─▄─▀█▄─██─▄█▄─█─▄███▄─▀█▄─▄█─▄▄─█▄─█▀▀▀█─▄███▄─▄▄─██▀▄─██▄─█─▄███▄─▄████▀▄─██─▄─▄─█▄─▄▄─█▄─▄▄▀█
██─▄─▀██─██─███▄─▄█████─█▄▀─██─██─██─█─█─█─█████─▄▄▄██─▀─███▄─▄█████─██▀██─▀─████─████─▄█▀██─▄─▄█
▀▄▄▄▄▀▀▀▄▄▄▄▀▀▀▄▄▄▀▀▀▀▄▄▄▀▀▄▄▀▄▄▄▄▀▀▄▄▄▀▄▄▄▀▀▀▀▄▄▄▀▀▀▄▄▀▄▄▀▀▄▄▄▀▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀
""")

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="BnowPlater"
)

mycursor = mydb.cursor()

# Create table if it doesn't exist
def initialize_database():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID BIGINT,
        Name VARCHAR(50),
        MobNo BIGINT,
        Email VARCHAR(100),
        Address VARCHAR(150),
        Balance BIGINT,
        PRIMARY KEY (CustomerID,MobNo)
    )"""
    mycursor.execute(create_table_sql)
    mydb.commit()
    print("Database initialized successfully")

def search(num):
    sql = f"SELECT * FROM customers WHERE MobNo = {num}"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return list(result[0]) if result else []

def cid():
    mycursor.execute("select max(customerid) from customers")
    ID = mycursor.fetchall()
    return 0 if ((ID[0])[0]) is None else ((ID[0])[0])

def addcust():
    print('New Customer Form:')
    custid = cid() + 1
    print(f'Customer ID: {custid}')
    
    while True:
        name = input('Enter Name(50char): ').upper()
        if name.isalpha() and len(name) <= 50:
            break
        print('Invalid customer Name')
    
    while True:
        num = input('Enter Mobile number: ')
        if num.isnumeric() and len(num) == 10:
            if not search(num):
                break
            print('Customer Already exists')
            return False
        print('Invalid Number')
    
    while True:
        email = input('Enter Email address(100char): ').lower()
        if '@' in email and '.com' in email and len(email) <= 100:
            break
        print('Invalid Email address')
    
    while True:
        addr = input('Enter Address(150char): ')
        if len(addr) <= 150:
            break
        print('Characters more than 150')

    sql = f"INSERT INTO CUSTOMERS (CustomerID,Name,MobNo,Email,Address) values({custid},'{name}',{num},'{email}','{addr}')"
    mycursor.execute(sql)
    mydb.commit()
    print(f'New customer {name} is added')
    return num

def display_customer(customer):
    balance = '0' if customer[5] in [0, None] else str(customer[5])
    return f"""
    Customer ID: {customer[0]}
    Customer Name: {customer[1]}
    Mobile Number: {customer[2]}
    Email address: {customer[3]}
    Address: {customer[4]}
    BALANCE: {balance}
    """

def update_balance(bal, num):
    sql = f'UPDATE Customers SET Balance = {bal} WHERE MobNo = {num}'
    mycursor.execute(sql)
    mydb.commit()

def pay():
    while True:
        num = input('Mobile Number: ')
        if num.isnumeric() and len(num) == 10:
            customer = search(num)
            if customer:
                print(display_customer(customer))
                if customer[5] not in [0, None]:
                    while True:
                        amount = input('Payment amount = ')
                        if amount.isnumeric() and len(amount) < 19:
                            amount = int(amount)
                            if customer[5] >= amount:
                                update_balance(customer[5] - amount, num)
                                print(f'Paid {amount} successfully')
                                print('Remaining balance:', search(num)[5])
                                return
                            print('Amount is higher than balance')
                            continue
                        print('Enter valid amount')
                print(f'{customer[1]} has Zero Balance')
                return
            print('Customer not found')
            if input("Exit or try again (e/t)? ").lower() == 'e':
                return
        else:
            print('Invalid number')

def lend():
    while True:
        num = input('Mobile Number: ')
        if num.isnumeric() and len(num) == 10:
            customer = search(num)
            if customer:
                print(display_customer(customer))
                current_balance = customer[5] if customer[5] is not None else 0
                while True:
                    amount = input('Loan amount = ')
                    if amount.isnumeric() and len(amount) < 19:
                        amount = int(amount)
                        if amount > 0:
                            update_balance(current_balance + amount, num)
                            print(f'Lent {amount} successfully')
                            print('New balance:', search(num)[5])
                            return
                        print("Can't enter zero amount")
                    print('Enter valid amount')
            print('Customer not found')
            choice = input("Exit, try again, or add new customer (e/t/add)? ").lower()
            if choice == 'e':
                return
            elif choice == 'add':
                if addcust():
                    print("New customer Added. Try entering the new number")
                    continue
                return
        else:
            print('Invalid number')

def custdetails():
    mycursor.execute("SELECT * FROM customers")
    customers = mycursor.fetchall()
    if not customers:
        print('No customers found')
    else:
        for customer in customers:
            print(display_customer(customer))

def delcust():
    while True:
        num = input('Mobile Number: ')
        if num.isnumeric() and len(num) == 10:
            customer = search(num)
            if customer:
                if input("Are you sure you want to delete the customer (y/n)? ").lower() == 'y':
                    mycursor.execute(f"DELETE FROM CUSTOMERS WHERE MobNo = {num}")
                    mydb.commit()
                    print('Customer Successfully Deleted')
                return
            print('Customer not found')
            if input('1.Try again\n2.Go back\n=>') != '1':
                return
        else:
            print('Invalid number')

def main():
    # Initialize database when program starts
    initialize_database()
    
    menu = """
    1. Lend
    2. Pay
    3. Search customer
    4. Customer list
    5. Add Customer
    6. Delete customer
    Enter "Exit" to Exit the Program
    """
    
    while True:
        print(menu)
        choice = input('=>')
        if choice.lower() == 'exit':
            print('Program closed\nThank you')
            break
        elif choice == '1':
            lend()
        elif choice == '2':
            pay()
        elif choice == '3':
            num = input('Mobile Number: ')
            if num.isnumeric() and len(num) == 10:
                customer = search(num)
                if customer:
                    print(display_customer(customer))
                else:
                    print('Customer not found')
            else:
                print('Invalid number')
        elif choice == '4':
            custdetails()
        elif choice == '5':
            addcust()
        elif choice == '6':
            delcust()
        else:
            print('Invalid input')

if __name__ == "__main__":
    main()
