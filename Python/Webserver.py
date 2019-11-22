import mysql.connector
import Config

if Config.debug["enabled"]:
    host = "172.20.10.12"
    user = "test"
    password = "test"
    database = "test"
else:
    host = Config.webServer["ip"]
    user = Config.webServer["user"]
    password = Config.webServer["password"]
    database = "test"

def connect(query): #Connect to mySQL server and send the message. Also handles errors
    try:
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        cursor = connection.cursor()
        result = cursor.execute(query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

    finally:
        if (connection.is_connected()):
            connection.close()

def InsertData(tabell, plassering, verdier): #Insert values in a database
    plassering = ", ".join(plassering)
    verdier = str(verdier).strip("[]")
    SQL_query = str(f"INSERT INTO {tabell} ({plassering}) VALUES ({verdier})")
    connect(SQL_query)

def UpdateData(tabell, plassering, verdier, nummer): #Update data at a given position in the databse
    SQL_query = str(f"UPDATE {tabell} SET ({plassering}) = ({verdier}) WHERE {nummer[0]} = {str(nummer[1])}")
    connect(SQL_query)

def DeleteData(tabell, plassering, verdier): #Delete data at a given position in the database
    SQL_query = str(f"DELETE FROM {tabell} WHERE ({plassering}) = ({verdier})")
    connect(SQL_query)

def ClearTable(tabell): #Clear the entire database
    SQL_query = str(f"DELETE FROM {tabell}")
    connect(SQL_query)

def CreateStoneTable(navn): #Create the database we will interact with
    SQL_query = str(f"CREATE TABLE {navn} (Nummer (INT), PosX (INT), PosY (INT), Farge(INT))")
    connect(SQL_query)

def CreateScoreTable(navn): #Create a database for keeping score (not used atm)
    SQL_query = str(f"CREATE TABLE {navn} (Kamp (INT), Lag1 (INT), Lag2 (INT))")
    connect(SQL_query)

