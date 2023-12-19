import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from portal import get_all_variables_from_db, get_variables_for_data_source, load_variable_data_from_db, visualize_variable_plotly, search_variable


# Home Page
def home():
    st.title("Data Portal App")
    st.write("Welcome to the Data Portal App. Explore, visualize, and download data!")

    st.write("""
    This app allows you to explore and analyze Zambian data from various sources. Here are the key features:

    1. **World Bank Page:** Explore data from the World Bank and visualize variables over time.

    2. **Bank of Zambia Page:** Upload Bank of Zambia data, view variables, and visualize data across time.

    3. **Zambia Statistics Agency Page:** Upload CSO inflation data, view variables and visualize data over time.

    4. **Stock Exchange Page:** Upload stock index data, view variables and visualize stock market trends.

    5. **Download Page:** Select variables, plot graphs, view tables, and export data as CSV.

    6. **Search Functionality:** Search for specific variables across all data sources. You must be very sure of the name of variable. See download page for reference.

    Explore the various pages using the sidebar navigation. If you have any questions or need assistance, feel free to reach out!

    Happy exploring!

     ---

    **About the Creator:**
    
    Hi, I'm Kampamba Shula, the creator of this app. Sofware Developer and Consultant.

    **Contact Information:**
    
    Feel free to reach out if you have any questions, feedback, or suggestions:
    
    - Email: kampambashula@gmail.com
    - LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/kampamba-shula-03946633/)
    - GitHub: [GitHub Profile](https://github.com/kshula)
    
    """)



    # Search Bar
    search_query = st.text_input("Search for a variable:")
    if st.button("Search"):
        # Implement search functionality here
        result = search_variable(search_query)

        if result is not None:
            # Display variable info
            st.write("### Variable Information")
            st.write(f"Variable Name: {result['variable_name']}")
            st.write(f"Data Source: {result['data_source']}")
            st.write(f"Start Year: {result['start_year']}")
            st.write(f"End Year: {result['end_year']}")

            # Offer the user the option to visualize the variable
            st.write("Do you want to visualize this variable?")
            visualize_option = st.radio("Select an option", ["Yes", "No"])

            if visualize_option == "Yes":
                # Visualize the variable using Plotly
                visualize_variable_plotly(result['data_source'], result['variable_name'])

            else:
                st.write("If you want to explore more, visit the Download Page.")

        else:
            st.write("Variable not found. Please check your spelling or try another variable.")
            st.write("Visit the Download Page to see the list of available variables.")



# World Bank Page
def world_bank_page():
    st.title("World Bank Page")

    # Placeholder for the selected variables
    selected_variables = []

    # Display list of all variables from the World Bank in the database
    all_world_bank_variables = get_variables_for_data_source('World Bank')
    selected_variables = st.multiselect("Select variables to plot:", all_world_bank_variables)
    # Check if the user has selected variables and clicked a button to visualize
    if st.button("Visualize Selected Variables"):
        # Iterate through selected variables and visualize each one
        for variable in selected_variables:
            visualize_variable_plotly('World Bank', variable)

# Bank of Zambia Page
def boz_page():
    st.title("Bank of Zambia Page")

    # Placeholder for the selected variables
    selected_variables = []

    # Display list of all variables from Bank of Zambia in the database
    all_boz_variables = get_variables_for_data_source('Bank of Zambia')
    selected_variables = st.multiselect("Select variables to plot:", all_boz_variables)
    # Check if the user has selected variables and clicked a button to visualize
    if st.button("Visualize Selected Variables"):
        # Iterate through selected variables and visualize each one
        for variable in selected_variables:
            visualize_variable_plotly('Bank of Zambia', variable)

# Zambia Statistics Agency Page
def cso_page():
    st.title("Zambia Statistics Agency Page")

    # Placeholder for the selected variables
    selected_variables = []

    # Display list of all variables from Zambia Statistics Agency in the database
    all_cso_variables = get_variables_for_data_source('Zambia Statistics Agency')
    selected_variables = st.multiselect("Select variables to plot:", all_cso_variables)

    # Check if the user has selected variables and clicked a button to visualize
    if st.button("Visualize Selected Variables"):
        # Iterate through selected variables and visualize each one
        for variable in selected_variables:
            visualize_variable_plotly('Zambia Statistics Agency', variable)


# Stock Exchange Page
def stock_exchange_page():
    st.title("Stock Exchange Page")

    # Placeholder for the selected variables
    selected_variables = []

    # Display list of all variables from Stock Exchange in the database
    all_stock_exchange_variables = get_variables_for_data_source('Stock Index')
    selected_variables = st.multiselect("Select variables to plot:", all_stock_exchange_variables)
    # Check if the user has selected variables and clicked a button to visualize
    if st.button("Visualize Selected Variables"):
        # Iterate through selected variables and visualize each one
        for variable in selected_variables:
            visualize_variable_plotly('Stock Index', variable)


# Download Page
def download_page():
    st.title("Download Data")

    # Placeholder for the selected variables
    selected_variables = []

    # Placeholder for the selected variable data
    selected_variable_data = pd.DataFrame()

    # Display list of all variables from the database
    all_variables = get_all_variables_from_db(selected_variables)
    selected_variables = st.multiselect("Select variables to plot:", all_variables)

    # Display selected variables
    if selected_variables:
        st.write("### Selected Variables:")
        st.write(selected_variables)

        # Allow user to choose how to display the data (plot, table, or both)
        display_option = st.radio("Select display option:", ["Plot", "Table", "Both"])

        # Plot selected variables
        if display_option in ["Plot", "Both"]:
            st.write("### Visualizing Selected Variables")
            for variable in selected_variables:
                # Placeholder for data loading (replace with actual data loading logic)
                variable_data = load_variable_data_from_db(variable)
                visualize_variable_plotly('your_data_source', variable)

                # Add data to the selected variable data placeholder
                selected_variable_data[variable] = variable_data['value']
                selected_variable_data['date'] = load_variable_data_from_db(variable)['date']
                

        # Table view of selected variables
        if display_option in ["Table", "Both"]:
            st.write("### Data Table")
            st.write(selected_variable_data)

        # Offer the option to export the table as CSV
        if st.button("Export Table as CSV"):
            # Export the table as CSV
            selected_variable_data.to_csv(f"{variable}_data.csv", index=False)
            st.write(f"Table for {variable} exported successfully.")


    else:
        st.write("Please select variables to plot.")

# App Navigation
if __name__ == "__main__":
    app_page = st.sidebar.selectbox("Select a page", ["Home", "World Bank", "Bank of Zambia", "CSO", "Stock Exchange", "Download"])

    if app_page == "Home":
        home()
    elif app_page == "World Bank":
        world_bank_page()
    elif app_page == "Bank of Zambia":
        boz_page()
    elif app_page == "CSO":
        cso_page()
    elif app_page == "Stock Exchange":
        stock_exchange_page()
    elif app_page == "Download":
        download_page()
