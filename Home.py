import streamlit as st
import pandas as pd
import altair as alt

st.header('Impact Product Positioning Sales', divider="grey")

data = pd.read_csv('Data/Product Positioning.csv')

filtered_data = data[(data['Product Category']=='Clothing')&
                     (data['Product Position'])]


st.write(filtered_data)

# Grouped bar chart using Altair
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='Product Position',
    y='mean(Price)',
    color='Seasonal',
    column='Seasonal'
).properties(
    width=200
)

st.write(chart)