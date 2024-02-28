import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



data = pd.read_csv('Data/Product Positioning.csv')



# --------------------------------------------------------------------
chart_data = data[(data['Promotion']=='Yes')&
                  (data['Product Category']=='Clothing')]
st.write(chart_data)
st.area_chart(chart_data, x='Product ID', y=['Price', "Competitor's Price"], color=["#FF0000", "#0000FF"])



#-----------------------------------
# Filtrer les colonnes de type 'object' autres que 'Product Category'
def visualize_data(data, x_column, y_column, xOffset_column, title):
    if xOffset_column != 'Product Category':
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(x_column, title='', axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'mean({y_column})'),
            xOffset=xOffset_column,
            color=alt.Color(xOffset_column, scale=alt.Scale(scheme='pastel1'))
        ).properties(
            width=600,
            height=400,
            title=title
        )
        st.altair_chart(chart, use_container_width=True, theme=None)
    else:
        pass

object_columns = data.select_dtypes(include='object').columns

for column in object_columns:
    visualize_data(data, 'Product Category', 'Sales Volume', column, f'Sales volume by Product category and {column}')





