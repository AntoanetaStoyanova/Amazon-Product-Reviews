import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.header('Impact Product Positioning Sales', divider="grey")

data = pd.read_csv('Data/Product Positioning.csv')

filtered_data = data[(data['Product Category']=='Clothing')&
                     (data['Product Position'])]






chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('Product Position', title=''),
    xOffset='Seasonal',
    y=alt.Y('mean(Price)'),
    color=alt.Color('Seasonal').scale(scheme='pastel1'))
st.altair_chart(chart, use_container_width=True, theme=None)





