# This file will fullfill all the dependencies
import mysql.connector as sqltor

# Making sql connection
mycon = sqltor.connect(user='root', password='pass123', host='127.0.0.1')
if not mycon.is_connected():
    print("Database is not connected")
    exit()


# Checking if db exists
myCursor = mycon.cursor()

def getConnection():
    return mycon, myCursor