import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Function to get all variables from the database
def get_all_variables_from_db(data_source):
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT variable FROM data')
    all_variables = [row[0] for row in cursor.fetchall()]

    conn.close()

    return all_variables

def get_variables_for_data_source(data_source):
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    # Fetch distinct variables for the specified data source
    cursor.execute('SELECT DISTINCT variable FROM data WHERE data_source = ?', (data_source,))
    variables = [row[0] for row in cursor.fetchall()]

    conn.close()

    return variables
# Function to load variable data from the database
def load_variable_data_from_db(variable):
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    cursor.execute('SELECT date, value FROM data WHERE variable = ?', (variable,))
    variable_data = pd.DataFrame(cursor.fetchall(), columns=['date', 'value'])

    conn.close()

    return variable_data

# Function to visualize the variable using Plotly
def visualize_variable_plotly(data_source, variable_name):
    st.write(f"### Visualizing {variable_name}")

    # Load data for visualization
    variable_data = load_variable_data_from_db(variable_name)

    # Check if data is available
    if not variable_data.empty:
        # Create a Plotly line chart
        fig = px.line(variable_data, x='date', y='value', title=f"{variable_name} over time")
        st.plotly_chart(fig)

    else:
        st.write(f"Data for {variable_name} from {data_source} is not available.")

# Function to search for a variable (replace with your actual search logic)
def search_variable(query):
    conn = sqlite3.connect('portal.db')
    cursor = conn.cursor()

    # Search for the variable in the database
    cursor.execute('''
        SELECT variable, data_source, MIN(date) AS start_year, MAX(date) AS end_year
        FROM data
        WHERE variable LIKE ? OR data_source LIKE ?
        GROUP BY variable, data_source
    ''', ('%' + query + '%', '%' + query + '%'))

    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            'variable_name': result[0],
            'data_source': result[1],
            'start_year': result[2],
            'end_year': result[3]
        }
    else:
        return None



