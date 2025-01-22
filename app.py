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

data['is_4wd']= data['is_4wd'].fillna(0)
data['is_4wd'] = data['is_4wd'].astype('bool')   
data['manufacturer']=data['model'].str.split().str[0]
data['paint_color']=data['paint_color'].fillna('unknown')
data['model_year'] = data['model_year'].fillna(data.groupby(['model'])['model_year'].transform('median')) 
data['odometer'] = data['odometer'].fillna(data.groupby(['model_year'])['odometer'].transform('median')) 
data['cylinders'] = data['cylinders'].fillna(data.groupby(['model'])['cylinders'].transform('median'))
data.sample(10)

# Vehicle listing analysis

st.title("Vehicle Listing Analysis")
st.sidebar.header("Filter by Vehicle Type")

# Selectbox to choose vehicle type
types = data['type'].unique()
selected_type = st.sidebar.selectbox("Select Vehicle type", types)

# Filter data based on vehicle type
filtered_data = data[data['type'] == selected_type]

# Display filtered data
st.write(f"Showing data for {selected_type}")
st.write(filtered_data)


# histogram for Price
st.subheader("Histogram: Price")
fig, ax = plt.subplots()
sns.histplot(filtered_data['price'], bins=10, kde=True, ax=ax)
ax.set_title("Distribution of Price")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Frequency")
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

### The goal here is to see how long are cars listed before they are sold

data['days_listed'].describe()

### It looks like most vehicles are sold around roughly 40 days!To sell cars faster the client should look to adjusting prices after the 45 day mark if vehicles have not sold.

# histogram of days listed
data['days_listed'].hist(bins = [5, 10, 40, 100, 150, 200])
plt.xlabel('days listed')
plt.ylabel('count of vehicles')
plt.title('Days listed before being sold')
plt.show()

# Group by 'category' and create histograms for 'value'
data.groupby('condition')['days_listed'].hist(bins=[20,40,60,80,100,120,140,160,180,200],alpha=0.7, legend=True)
plt.show()

### It also appears that there is a steep decline in excellent condition vehicles as time passes. 