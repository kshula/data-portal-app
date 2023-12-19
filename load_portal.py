import pandas as pd
import sqlite3

def create_table():
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_source TEXT,
            variable TEXT,
            date DATE,
            value FLOAT
        )
    ''')

    conn.commit()
    conn.close()

def import_data(file_path, data_source):
    data = pd.read_csv(file_path)
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    create_table()

    for variable in data.columns[1:]:
        for date, value in zip(data[data.columns[0]], data[variable]):
            cursor.execute('''
                INSERT INTO data (data_source, variable, date, value)
                VALUES (?, ?, ?, ?)
            ''', (data_source, variable, date, value))

    conn.commit()
    conn.close()

    print(f"Data imported into the database for {data_source}.")

# Example usage for one CSV file (repeat for other CSV files)
import_data('CSV\wb.csv', 'World Bank')
import_data('CSV\stock_index.csv', 'Stock Index')
import_data('CSV\cso_inflation.csv', 'Zambia Statistics Agency')
import_data('CSV\\boz_rate.csv', 'Bank of Zambia')
import_data('CSV\\boz_money.csv', 'Bank of Zambia')
import_data('CSV\\boz_mobile.csv', 'Bank of Zambia')
import_data('CSV\\boz_loan.csv', 'Bank of Zambia')
import_data('CSV\\boz_balance.csv', 'Bank of Zambia')
import_data('CSV\\boz_assets.csv', 'Bank of Zambia')