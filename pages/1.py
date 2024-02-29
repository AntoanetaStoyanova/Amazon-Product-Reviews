import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit import altair_chart


from st_pages import visualize_data, dataset, count_promotion_sales, count_position_sales, count_position_sales_clothing, count_position_sales_electronics, count_position_sales_food 



st.set_page_config(layout="wide")
data = pd.read_csv('Data/Product Positioning.csv')



object_columns = data.select_dtypes(include='object').columns

# Organizing the visualizations into 2 rows and 2 columns
st.write('## Visualizations')

col1, col2 = st.columns([1, 1])
with col1:
    altair_chart(visualize_data(data, 'Product Category', 'Sales Volume', object_columns[0], f'Sales volume by Product category and {object_columns[0]}'), use_container_width=True)
    altair_chart(visualize_data(data, 'Product Category', 'Sales Volume', object_columns[1], f'Sales volume by Product category and {object_columns[1]}'), use_container_width=True)
    altair_chart(visualize_data(data, 'Product Category', 'Sales Volume', object_columns[2], f'Sales volume by Product category and {object_columns[2]}'), use_container_width=True)
    altair_chart(visualize_data(data, 'Product Category', 'Sales Volume', object_columns[3], f'Sales volume by Product category and {object_columns[3]}'), use_container_width=True)
    # --------------------------------------------------------------------
    # Average Price by Position and Seasonal Product
    filtered_data = data[(data['Product Category']=='Clothing')]
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('Product Position', title='', axis=alt.Axis(labelAngle=0)),
        xOffset='Seasonal',
        y=alt.Y('mean(Price)'),
        color=alt.Color('Seasonal').scale(scheme='pastel1')
    ).properties(
        width=600,
        height=350,
        title='Average Price by Position and Seasonal Product'
    )
    st.altair_chart(chart, use_container_width=True, theme=None)
    # --------------------------------------------------------------------
with col2:
    #------------------------
    option = st.selectbox(
        'Choose a Product Category:',
        ('Clothing', 'Electronics', 'Food'))
    # define a dictionnart ( map eaxh product category to a list of tab labels associated with that category). allows to retrieve the tab labels based on the selection option later
    tab_labels = {'Clothing': ['Aisle', 'End-cap', 'Front of Store'],
                'Electronics': ['Aisle', 'End-cap', 'Front of Store'],
                'Food': ['Aisle', 'End-cap', 'Front of Store']}

    if option:
        selected_data = dataset(data, option)
        # create tabs and pass the list of tab labels corresponding to the selected option
        tabs = st.tabs(tab_labels[option])
        # loop that iterates over each tab label in the list of tab labels associated with the selected option.
        # enumerate() to get both the index (i) and the tab label in each iteration
        for i, tab_label in enumerate(tab_labels[option]):
            # set current tab to the tab at index i 
            with tabs[i]:
                count_position_sales(data, option, tab_label)
    #------------------------









    # Creating tabs
    tab7, tab8, tab9 = st.tabs(['Aisle', 'End-cap', 'Front of Store'])
    # Processing each tab
    with tab7:
        count_promotion_sales(data, 'Aisle')
    with tab8:
        count_promotion_sales(data, 'End-cap')
    with tab9:
        count_promotion_sales(data, 'Front of Store')

    #-----------------
    filtered_data_clothing = data[data['Product Category'] == 'Clothing']

    # Filter the data for seasonal promotional clothing
    sales_volume = filtered_data_clothing[(filtered_data_clothing['Seasonal'] == 'Yes') & (filtered_data_clothing['Promotion'] == 'Yes')]
    # Strip whitespace from 'Product Position'
    sales_volume['Product Position'] = sales_volume['Product Position'].str.strip()
    # Get the total number of clothing products
    total_clothing_products = len(sales_volume)
    # Group by 'Product Position' and sum up the 'Sales Volume'
    position_sales_volume = sales_volume.groupby('Product Position')['Sales Volume'].sum().reset_index()
    
    st.write("Total sales volume for each product position category for seasonal promotional clothing:")
    st.write(position_sales_volume)

    fig = px.pie(position_sales_volume, names='Product Position', values='Sales Volume')
    st.write(fig)


