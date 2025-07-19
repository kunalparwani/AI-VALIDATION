import os



import sqlite3







def login(username, password):



    conn = sqlite3.connect('users.db')



    cursor = conn.cursor()



    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';"



    cursor.execute(query)



    result = cursor.fetchone()



    if result:



        print("Login successful!")



    else:



        print("Login failed.")







def delete_file():



    filename = input("Enter filename to delete: ")



    os.system("rm " + filename)



