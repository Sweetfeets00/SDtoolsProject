import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px

# Load data
data = pd.read_csv('/Users/deshawncouch/SDtoolsProject/vehicles_us.csv')

# Data overview and cleaning
st.title("Vehicle Listing Analysis")

buffer = []
data.info(buf=buffer.append)
st.text("\n".join(buffer))
st.write(f"Number of duplicated rows: {data.duplicated().sum()}")

# Handle missing values
data['is_4wd'] = data['is_4wd'].fillna(0).astype('bool')
data['model_year'] = data['model_year'].fillna(data['model_year'].median()).astype('int')
data['odometer'] = data['odometer'].fillna(data['odometer'].median()).astype('int')
data['cylinders'] = data['cylinders'].fillna(data['cylinders'].median()).astype('int')

# Extract manufacturer
data['manufacturer'] = data['model'].str.split().str[0]

# Define categories for condition
condition_order = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
data['condition'] = pd.Categorical(data['condition'], categories=condition_order, ordered=True)

# Sidebar filters
st.sidebar.header("Filters")
manufacturers = data['manufacturer'].unique()
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers)

price_min, price_max = st.sidebar.slider(
    "Select Price Range", int(data['price'].min()), int(data['price'].max()), (5000, 20000)
)

# Filter data
filtered_data = data[(data['manufacturer'] == selected_manufacturer) &
                     (data['price'] >= price_min) &
                     (data['price'] <= price_max)]

st.write(f"Showing data for {selected_manufacturer} within price range ${price_min} - ${price_max}")
st.write(filtered_data)

# Histogram: Days Listed
st.subheader("Histogram: Days Listed")
fig, ax = plt.subplots()
sns.histplot(filtered_data['days_listed'], bins=10, kde=True, ax=ax)
ax.set_title("Distribution of Days Listed")
ax.set_xlabel("Days Listed")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Histogram: Price
st.subheader("Histogram: Price")
fig, ax = plt.subplots()
sns.histplot(filtered_data['price'], bins=10, kde=True, ax=ax)
ax.set_title("Distribution of Price")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Bar Chart: Condition
st.subheader("Bar Chart: Condition")
fig, ax = plt.subplots()
sns.countplot(x='condition', data=filtered_data, order=condition_order, ax=ax)
ax.set_title("Condition Distribution")
ax.set_xlabel("Condition")
ax.set_ylabel("Count")
st.pyplot(fig)

# Scatterplot: Condition vs. Days Listed
st.subheader("Scatterplot: Condition vs. Days Listed")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_data, x='days_listed', y='condition', hue='condition', s=100, ax=ax)
ax.set_title("Scatterplot: Condition vs. Days Listed")
ax.set_xlabel("Days Listed")
ax.set_ylabel("Condition")
st.pyplot(fig)

# Missing Data Heatmap
st.subheader("Missing Data Heatmap")
fig, ax = plt.subplots()
sns.heatmap(data.isna(), cbar=False, ax=ax)
ax.set_title("Missing Data Heatmap")
st.pyplot(fig)
