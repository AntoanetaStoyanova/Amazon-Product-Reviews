import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_data(data, x_column, y_column, xOffset_column, title):
    if xOffset_column != 'Product Category':
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(x_column, title='', axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'mean({y_column})'),
            xOffset=xOffset_column,
            color=alt.Color(xOffset_column, scale=alt.Scale(scheme='pastel1'))
        ).properties(
            width=600,  # Adjust width for 3 columns
            height=350, # Adjust height for 2 rows
            title=title
        )
        return chart

def dataset(data, category):

    filtered_data_clothing = data[data['Product Category'] == category]
    st.write(f'% of Sales Volume of {category} Item by Product Position:')
    
    # Group by 'Product Position' and calculate total sales value
    position_sales = filtered_data_clothing.groupby('Product Position')['Sales Volume'].sum()
    # Calculate total sales value for all positions
    total_sales = position_sales.sum()
    # Calculate percentage of sales value for each position
    position_sales_percentage = round((position_sales / total_sales) * 100, 2)
    #st.write(position_sales_percentage)
        # Création d'un dictionnaire à partir de position_sales_percentage
    data_dict = {'Product Position': position_sales_percentage.index, '% Sales Volume': position_sales_percentage.values}

    # Création de la DataFrame
    df = pd.DataFrame(data_dict)

        # Affichage de la DataFrame
    st.write(df)



#----------
# Product Category Selector with Seasonal Flag: Analyzing Promo vs Non-Promo Sales Volume by Product Position
def calculate_sales(data):
    promo_sales = data[data['Promotion'] == 'Yes']['Sales Volume'].sum()
    non_promo_sales = data[data['Promotion'] == 'No']['Sales Volume'].sum()
    return promo_sales, non_promo_sales

def display_sales_data(data, category, seasonal, selected_option):
    if data is not None: # checks if the data parameter is not None
        
        st.write(f'{seasonal} Product Category: {category}')
        df = pd.DataFrame({
            'Product Category': [category],
            'Sales Values': [data if data else 0], # if data is not None, the value will be set to the value of data
            'Seasonal': [seasonal]
        })
        st.write(df)
        
def process_seasonal_data(data, category, selected_option):
    # group the data by Seasonal col and calculate the sum of Sales Volume for each Seasonal category 
    seasonal_sales = data.groupby('Seasonal')['Sales Volume'].sum()
    # call the display_sales_data function 
    # passe the sum of Sales volume for seasonal products along with Product Category and Selected option [Seasonal, Unseasonal]
    display_sales_data(seasonal_sales.get('Yes'), category, 'seasonal', selected_option)
    display_sales_data(seasonal_sales.get('No'), category, 'unseasonal', selected_option)

    # extract unique position from ['Product Position']
    unique_positions = data['Product Position'].unique()
    # create a list of strings representing the position categories 
    position_strings = [str(position) for position in unique_positions]
    # generate tabs 
    tabs = st.tabs(position_strings)
    
    # for each position, filter the data for the position and calculates promotional and non-promo sales using the func calculate_sales()
    for i, position in enumerate(unique_positions):
        position_data = data[data['Product Position'] == position]
        promo_sales, non_promo_sales = calculate_sales(position_data)
        with tabs[i]:
            st.write(f"Sales Volume for Promo items in {position}: ", promo_sales)
            st.write(f"Sales Volume for Non-Promo items in {position}: ", non_promo_sales)

def dataset_seasonable(data, category, option, selected_option):
    filtered_data = data[data['Product Category'] == category]
    
    if option == 'Seasonal':
        seasonal_data = filtered_data[filtered_data['Seasonal'] == 'Yes']
        process_seasonal_data(seasonal_data, category, selected_option)
    else:
        unseasonal_data = filtered_data[filtered_data['Seasonal'] == 'No']
        process_seasonal_data(unseasonal_data, category, selected_option) 
#-------------




def count_position_sales(data, category, position):
    # Filter data based on position and category
    filtered_data = data[(data['Product Category'] == category) & (data['Product Position'] == position)]
        
    # Calculate seasonal sales counts
    seasonal_yes_count = filtered_data[filtered_data['Seasonal'] == 'Yes']['Sales Volume'].sum()
    seasonal_no_count = filtered_data[filtered_data['Seasonal'] == 'No']['Sales Volume'].sum()
        
    # Calculate percentages
    total_sales = seasonal_yes_count + seasonal_no_count
    percentage_yes = round((seasonal_yes_count / total_sales) * 100, 2)
    percentage_no = round((seasonal_no_count / total_sales) * 100, 2)
        
    # Output results
    st.write(f"Store Sales of Seasonal {category} Items:   sales volume:", seasonal_yes_count, ",  ", percentage_yes, " %")
    st.write(f"Store Sales of Non-seasonal {category} Items:   sales volume:", seasonal_no_count, ",  ", percentage_no, " %")





#------------------------------------------------------------
def analyze_sales(data, category, group_by):
    filtered_data_clothing = data[data['Product Category'] == category]
    
    if group_by == 'Product Position':
        st.write(f'% of Sales Volume of {category} Item by Product Position:')
    elif group_by == 'Foot Traffic':
        st.write(f'% of Sales Volume of {category} Item by Foot Traffic:')
    elif group_by == 'Consumer Demographics':
        st.write(f'% of Sales Volume of {category} Item by Consumer Demographics:')
    else:
        st.write("Invalid group by criterion!")
        return
    
    # Group by the specified criterion and calculate total sales value
    sales_by_group = filtered_data_clothing.groupby(group_by)['Sales Volume'].sum()
    total_sales = sales_by_group.sum()
    sales_percentage = round((sales_by_group / total_sales) * 100, 2)

    # Create a dictionary from sales_percentage
    data_dict = {group_by: sales_percentage.index, '% Sales Volume': sales_percentage.values}

    # Create a DataFrame
    df = pd.DataFrame(data_dict)

    # Display the DataFrame
    st.write(df)