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

def count_position_sales_clothing(data, position, category='Clothing'):
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
    st.write("Store Sales of Seasonal Clothing Items:   sales volume:", seasonal_yes_count, ",  ", percentage_yes, " %")
    st.write("Store Sales of Non-seasonal Clothing Items:   sales volume:", seasonal_no_count, ",  ", percentage_no, " %")

def count_position_sales_electronics(data, position, category='Electronics'):
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
    st.write("Store Sales of Seasonal Electronics Items:   sales volume:", seasonal_yes_count, ",  ", percentage_yes, " %")
    st.write("Store Sales of Non-seasonal Electronics Items:   sales volume:", seasonal_no_count, ",  ", percentage_no, " %")

def count_position_sales_food(data, position, category='Food'):
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
    st.write("Store Sales of Seasonal Food Items:   sales volume:", seasonal_yes_count, ",  ", percentage_yes, " %")
    st.write("Store Sales of Non-seasonal Food Items:   sales volume:", seasonal_no_count, ",  ", percentage_no, " %")

def count_promotion_sales(data, position):
    # Filter data based on position and category
    filtered_data_seasonal = data[(data['Product Category'] == 'Clothing')&(data['Product Position'] == position)]
    
    promotion_yes = filtered_data_seasonal[(filtered_data_seasonal['Seasonal'] == 'Yes')&(filtered_data_seasonal['Promotion']=='Yes')]['Sales Volume'].sum()
    promotion_non = filtered_data_seasonal[(filtered_data_seasonal['Seasonal'] == 'No')&(filtered_data_seasonal['Promotion']=='Yes')]['Sales Volume'].sum()
    # Calculate percentages
    total_promotion = promotion_yes + promotion_non
    percentage_yes_promo = round((promotion_yes / total_promotion) * 100, 2)
    percentage_no_promo = round((promotion_non / total_promotion) * 100, 2)
    st.write("Total Sales Volume for Seasonal Clothing Items on Promotion:  sales values:", promotion_yes, '  ,', percentage_yes_promo, ' %')
    st.write("Total Sales Volume for Non-seasonal Clothing Items on Promotion:  sales values:", promotion_non, '  ,', percentage_no_promo, ' %')