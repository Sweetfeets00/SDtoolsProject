import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly.express as px
import seaborn as sns

datap = pd.read_csv('./datap.csv')

# Vehicle listing analysis

st.title("Vehicle Listing Analysis")
st.sidebar.header("Filter by Manufacturer")

# Selectbox to choose vehicle manufacturer
manufacturers = datap['manufacturer'].unique()
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers)

# Filter data based on manufacturer
filtered_data = datap[datap['manufacturer'] == selected_manufacturer]

# Display filtered data
# st.write(f"Showing data for {selected_manufacturer}")
# st.write(filtered_data)

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
manufacturers = datap['manufacturer'].unique()
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers,key="manufacturer_selectbox")

# Filter data based on manufacturer
filtered_data = datap[datap['manufacturer'] == selected_manufacturer]

# filtered data
# st.write(f"Showing data for {selected_manufacturer}")
# st.write(filtered_data)

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


### It looks like most vehicles are sold around roughly 40 days!To sell cars faster the client should look to adjusting prices after the 45 day mark if vehicles have not sold.

# histogram of days listed
g = sns.FacetGrid(datap, col="condition", col_wrap=3, sharex=True, sharey=True)

# Map histogram to the FacetGrid
g.map(plt.hist, "days_listed", bins=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200], alpha=0.7)

# Set labels and title
g.set_axis_labels("Days Listed", "Frequency")
g.fig.suptitle("Days Listed by Vehicle Condition", y=1.02)

# Show the plot
plt.show()

# Group by 'category' and create histograms for 'value'
datap.groupby('condition')['days_listed'].hist(bins=[20,40,60,80,100,120,140,160,180,200],alpha=0.7, legend=True)
plt.show()

### It also appears that there is a steep decline in excellent condition vehicles as time passes. 

fig = px.scatter(datap,
    x='price',
    y='days_listed',
    color='condition',
    size='price',  # Size the markers by price
    hover_data=['condition'],
    title='Scatterplot: Price vs Days Listed by Condition'
)
fig.update_layout(
    xaxis_title='Price ($)',
    yaxis_title='Days Listed'
)
fig.show()

## Based on the above it also appears that cheaper vehicles sell faster and more expensive vehicles still sell in about 40 days regardless of condition