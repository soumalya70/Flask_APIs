from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'flask_db'
}

def fetch_data(ticker, columns=None, period=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    if columns and period:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*int(period[0]))
        query = f"SELECT ticker, date, {', '.join(columns)} FROM data WHERE ticker = '{ticker}' AND date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"
    elif columns:
        query = f"SELECT ticker, date, {', '.join(columns)} FROM data WHERE ticker = '{ticker}'"
    else:
        query = f"SELECT * FROM data WHERE ticker = '{ticker}'"

    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

@app.route('/Api/ticker=<ticker>', methods=['GET'])
def get_data_ticker(ticker):
    data = fetch_data(ticker)
    return jsonify(data)

@app.route('/Api/ticker=<ticker>&column=<columns>', methods=['GET'])
def get_data_ticker_columns(ticker, columns):
    columns = columns.split(',')
    data = fetch_data(ticker, columns)
    return jsonify(data)

@app.route('/Api/ticker=<ticker>&column=<columns>&period=<period>', methods=['GET'])
def get_data_ticker_column_period(ticker, columns, period):
    columns = columns.split(',')
    data = fetch_data(ticker, columns, period)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
