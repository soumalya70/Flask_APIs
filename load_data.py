import csv
import mysql.connector
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': '', 
    'database': 'Flask_db'  
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS data (
    ticker VARCHAR(255),
    date DATE,
    revenue INT,
    gp INT,
    fcf INT,
    capex INT
)
"""
cursor.execute(create_table_query)

with open("Sample-Data-Historic.csv", 'r') as f:
    csv_data = csv.reader(f)
    next(csv_data)  
    for row in csv_data:
        date_str = row[1]  
        date_obj = datetime.strptime(date_str, '%m/%d/%Y') 
        formatted_date = date_obj.strftime('%Y-%m-%d')
        row[1] = formatted_date
        query = "INSERT INTO data (ticker, date, revenue, gp, fcf, capex) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, row)

connection.commit()
cursor.close()
connection.close()

print("CSV data uploaded successfully")


