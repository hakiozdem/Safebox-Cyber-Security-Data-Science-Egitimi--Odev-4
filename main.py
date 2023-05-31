# -*- coding: utf-8 -*-
import pyodbc

server = 'DESKTOP-VVUOOEK' # 10.40.1.11
database = '....'
username = '....'
password = '....'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def show_products():
    cursor.execute("execute show_products")
    products = cursor.fetchall()
    for i in range(len(products)):
        print(str(i)+". "+products[i][0])
    return products

def user_actions(username):
    options = "1.List All Products\n2. Buy a Product\nq:logout"
    while(True):
        print(options)
        option= input("Select option: ")
        if option == "1":
            show_products()
        elif option == "2":
            products = show_products()
            product_id = int(input("Which product you want to buy? as number"))
            cursor.execute("execute buy ?,?",(product_id,username))
        elif option=="q":
            print("Good Bye!")
            break
        
            
            
    

options = "1.Login\n2.Register\nq:Quit"
while(True):
    print(options)
    selection = input("Select an option: ")
    print("******************")
    if selection=="1":
        username = input("Username= ")
        password = input("Password= ")
        cursor.execute("execute dbo.login ?,?",(username,password))
        login_val=cursor.fetchone()
        print(type(login_val[0]))
        if login_val[0]==1:
            print("******************")
            print("Welcome "+username)
            print("******************")
            user_actions(username)
        else:
            print("Wrong username or password")
    if selection == "2":
        username = input("Username= ")
        password = input("Password= ")
        email = input("Email= ")
        cursor.execute("execute add_user ?,?,?",(username,email,password))
        print("User created successfully")
    
    if selection=="q":
        print("thanks for using!!!")
        cursor.close()
        cnxn.close()
        break
        


    
    