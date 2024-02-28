import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit import altair_chart


from st_pages import visualize_data, dataset, count_promotion_sales, count_position_sales_clothing, count_position_sales_electronics, count_position_sales_food 



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
#-----------------
    tab1, tab2, tab3 = st.tabs(['Clothing', 'Electronics', 'Food'])
    # Processing each tab
    with tab1:
        dataset(data, 'Clothing')
         # Creating tabs
        tab6, tab7, tab8 = st.tabs(['Aisle', 'End-cap', 'Front of Store'])
        # Processing each tab
        with tab6:
            count_position_sales_clothing(data, 'Aisle')
        with tab7:
            count_position_sales_clothing(data, 'End-cap')
        with tab8:
            count_position_sales_clothing(data, 'Front of Store')
    with tab2:
        dataset(data, 'Electronics')
         # Creating tabs
        tab6, tab7, tab8 = st.tabs(['Aisle', 'End-cap', 'Front of Store'])
        # Processing each tab
        with tab6:
            count_position_sales_electronics(data, 'Aisle')
        with tab7:
            count_position_sales_electronics(data, 'End-cap')
        with tab8:
            count_position_sales_electronics(data, 'Front of Store')
    with tab3:
        dataset(data, 'Food')
         # Creating tabs
        tab9, tab10, tab11 = st.tabs(['Aisle', 'End-cap', 'Front of Store'])
        # Processing each tab
        with tab9:
            count_position_sales_food(data, 'Aisle')
        with tab10:
            count_position_sales_food(data, 'End-cap')
        with tab11:
            count_position_sales_food(data, 'Front of Store')




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


