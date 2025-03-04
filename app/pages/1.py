import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit import altair_chart



from st_pages import visualize_data, dataset_seasonable, count_position_sales, analyze_sales



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
    st.markdown('##### Product Category Selector: Analyzing the % of Sales Volume of Product Category by Product Position and is it Seasonal or not')

    option = st.selectbox(
        'Choose a Product Category:',
        ('Clothing', 'Electronics', 'Food'))
    # define a dictionnart ( map eaxh product category to a list of tab labels associated with that category). allows to retrieve the tab labels based on the selection option later
    tab_labels = {'Clothing': ['Aisle', 'End-cap', 'Front of Store'],
                'Electronics': ['Aisle', 'End-cap', 'Front of Store'],
                'Food': ['Aisle', 'End-cap', 'Front of Store']}

    if option:
        selected_data = analyze_sales(data, option, 'Product Position')
        # create tabs and pass the list of tab labels corresponding to the selected option
        tabs = st.tabs(tab_labels[option])
        # loop that iterates over each tab label in the list of tab labels associated with the selected option.
        # enumerate() to get both the index (i) and the tab label in each iteration
        for i, tab_label in enumerate(tab_labels[option]):
            # set current tab to the tab at index i 
            with tabs[i]:
                count_position_sales(data, option, tab_label)
    #------------------------
    # ----------------------
    # Add blank space 
    st.markdown("<br>", unsafe_allow_html=True)
    # ----------------------
    st.divider()
    st.markdown('##### Product Category Selector with Seasonal Flag: Analyzing Promo vs Non-Promo Sales Volume by Product Position')
    option_seasonal_promo = st.selectbox('Choose a Product Category:', ('Clothing', 'Electronics', 'Food'), key="seasonal_promo_option")
    option_s = st.radio (f'Sales Volume of {option_seasonal_promo}:', ['Seasonal', 'Unseasonal'], horizontal=True)
    
    selected_option = None  # You need to define selected_option here
    # PROBLEM
    if option_seasonal_promo:
        dataset_seasonable(data, option_seasonal_promo, option_s, selected_option)
    st.divider()
        
    
    # ----------------------
    # Add blank space 
    st.markdown("<br>", unsafe_allow_html=True)
    # ----------------------

    option_ft = st.selectbox('Choose a Product Category:', ('Clothing', 'Electronics', 'Food'), key="ft")
    if option_ft:
        analyze_sales(data, option_ft, 'Foot Traffic')

    st.divider()
    #-----------------
        
        # ----------------------
    # Add blank space 
    st.markdown("<br>", unsafe_allow_html=True)
    # ----------------------

    option_cd = st.selectbox('Choose a Product Category:', ('Clothing', 'Electronics', 'Food'), key="cd")
    if option_cd:
        analyze_sales(data, option_cd, 'Consumer Demographics')
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


