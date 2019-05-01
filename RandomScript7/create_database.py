import sqlite3
from csvtools import *
import re
import os

if os.path.isfile("Database/nagwa.db"):
    os.remove("Database/nagwa.db")

eldpl = readCSVAsList("Data/eldpl.csv") # english lesson details per lesson
lie = readCSVAsList("Data/lie.csv") # lessons in english
llqpq = readCSVAsList("Data/llqpq.csv") # lesson linked questions per question
qcd = readCSVAsList("Data/qcd.csv") # question creator details
sif = readCSVAsList("Data/sif.csv") # singles in flow
wie = readCSVAsList("Data/wie.csv") # worksheets in english

def correctId(id):
    if re.match(r"=\"\d{12}\"", id):
        return id[2:-1]
    else:
        return id

def isInteger(text):
    return re.match(r"^\d+$", text)

def isReal(text):
    return re.match(r"^\d+(\.\d+)?$", text)

def getColumnType(cell):
    if isReal(cell):
        return "real"
    else:
        return "text"

def getColumnTypes(row):
    return [getColumnType(c) for c in row]


def makeTableFromCSVData(cursor, name, rows):
    headers = rows[0]
    columnTypes = getColumnTypes(rows[1])
    
    headers = [re.sub(r"[^A-Za-z0-9]", "", h) + " " + c for h, c in zip(headers, columnTypes)]
    headers_text = ", ".join(headers)
    number_of_columns = len(headers)

    print(headers_text)

    cursor.execute("CREATE TABLE {0} ({1})".format(name, headers_text ))

    for row in rows[1:]:
        n = len(row)
        if n == number_of_columns + 1:
            row = row[:-1]
        if n == number_of_columns - 1:
            row = row  +[""]

        row = [correctId(c) for c in row]
        
        row_text =  ",".join( ["'" + re.sub(r"[']", "''", c) + "'" for c in row])
        print row_text

        cursor.execute("INSERT INTO {0} VALUES ({1})".format(name, row_text))


connection = sqlite3.connect("Database/nagwa.db")
cursor = connection.cursor()

makeTableFromCSVData(cursor, "eldpl", eldpl)
makeTableFromCSVData(cursor, "lie", lie)
makeTableFromCSVData(cursor, "llqpq", llqpq)
makeTableFromCSVData(cursor, "qcd", qcd)
makeTableFromCSVData(cursor, "sif", sif)
makeTableFromCSVData(cursor, "wie", wie)

connection.close()