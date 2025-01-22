import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly.express as px
import seaborn as sns

data = pd.read_csv('./vehicles_us.csv')

data.info()

data.duplicated().sum()

data['is_4wd']= data['is_4wd'].fillna(0)
data['is_4wd'] = data['is_4wd'].astype('bool') 
data['manufacturer']=data['model'].str.split().str[0]
data['paint_color']=data['paint_color'].fillna('unknown')
data['model_year'] = data['model_year'].fillna(data.groupby(['model'])['model_year'].transform('median')) 
data['odometer'] = data['odometer'].fillna(data.groupby(['model_year'])['odometer'].transform('median')) 
data['cylinders'] = data['cylinders'].fillna(data.groupby(['model'])['cylinders'].transform('median'))

### The goal here is to see how long are cars listed before they are sold

data['days_listed'].describe()

### It looks like most vehicles are sold around roughly 40 days!To sell cars faster the client should look to adjusting prices after the 45 day mark if vehicles have not sold.

# histogram of days listed
g = sns.FacetGrid(data, col="condition", col_wrap=3, sharex=True, sharey=True)
g.map(plt.hist, "days_listed", bins=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200], alpha=0.7)
g.set_axis_labels("Days Listed", "Frequency")
g.fig.suptitle("Days Listed by Vehicle Condition", y=1.02)
plt.show()

# Group by 'category' and create histograms for 'value'
data.groupby('condition')['days_listed'].hist(bins=[20,40,60,80,100,120,140,160,180,200],alpha=0.7, legend=True)
plt.show()

### It also appears that there is a steep decline in excellent condition vehicles as time passes. 

fig = px.scatter(
    data,
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

## Based on the above it also appears that cheaper vehicles sell faster and more expensive vehicles still sell in about 40 days regardless of condiiton