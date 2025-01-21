import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly.express as px
import seaborn as sns

data = pd.read_csv('/Users/deshawncouch/SDtoolsProject/vehicles_us.csv')

data.info()

data.duplicated().sum()

data.head(50)
data['model_year'].isna().sum()
data['is_4wd']= data['is_4wd'].fillna(0)
data['is_4wd'] = data['is_4wd'].astype('bool')
data['model_year']= data['model_year'].fillna(0)
data['model_year']= data['model_year'].astype('int')
data['odometer']=data['odometer'].fillna(0)
data['odometer']=data['odometer'].astype('int')
data['cylinders']=data['cylinders'].fillna(0)   
data['cylinders']=data['cylinders'].astype('int')   
data['manufacturer']=data['model'].str.split().str[0]
data.sample(50)

# Vehicle listing analysis

st.title("Vehicle Listing Analysis")
st.sidebar.header("Filter by Manufacturer")

# Selectbox to choose vehicle manufacturer
manufacturers = data['manufacturer'].unique()
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers)

# Filter data based on manufacturer
filtered_data = data[data['manufacturer'] == selected_manufacturer]

# Display filtered data
st.write(f"Showing data for {selected_manufacturer}")
st.write(filtered_data)

# histogram for Days Listed
st.subheader("Histogram: Days Listed")
fig, ax = plt.subplots()
sns.histplot(filtered_data['days_listed'], bins=10, kde=True, ax=ax)
ax.set_title("Distribution of Days Listed")
ax.set_xlabel("Days Listed")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# histogram for Price
st.subheader("Histogram: Price")
fig, ax = plt.subplots()
sns.histplot(filtered_data['price'], bins=10, kde=True, ax=ax)
ax.set_title("Distribution of Price")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# histogram for Condition
st.subheader("Histogram: Condition")
fig, ax = plt.subplots()
sns.countplot(x='condition', data=filtered_data, ax=ax)
ax.set_title("Condition Distribution")
st.pyplot(fig)

# Correlation between condition and Days listed 

st.title("Correlation Analysis")
st.sidebar.header("Filter by Manufacturer")

# Selectbox to choose vehicle manufacturer
manufacturers = data['manufacturer'].unique()
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers,key="manufacturer_selectbox")

# Filter data based on manufacturer
filtered_data = data[data['manufacturer'] == selected_manufacturer]

# filtered data
st.write(f"Showing data for {selected_manufacturer}")
st.write(filtered_data)

# Scatterplot: Condition vs. Days Listed
st.subheader("Scatterplot: Condition vs. Days Listed")

# scatterplot seaborn
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_data, x='days_listed', y='condition', hue='condition', style='condition', s=100, ax=ax)

# titles and labels
ax.set_title("Scatterplot: Condition vs. Days Listed")
ax.set_xlabel("Days Listed")
ax.set_ylabel("Condition")

# Show the plot in Streamlit
st.pyplot(fig)