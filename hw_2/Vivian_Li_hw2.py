#!/usr/bin/env python
# coding: utf-8

# # Homework 2
# ## DS 3000: Foundation of Data Science
# Name: Vivian Shu Yi Li <br>
# NUID: 001506227 <br>
# Date: May 31, 2023 <br>

# ## Upload libraries and filter dataset

# In[1]:


# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import plotly.express as px
import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap


# In[2]:


def read_file(filename):
    """ reading csv file
    Args:
        filename (str): csv file
    
    Return:
        dataframe of the filtered csv file
    """
    # read the csv file
    crime = pd.read_csv(filename)
    
    # delete unnecessary cols
    del_col = ['OFFENSE_DESCRIPTION', 'DISTRICT', 'REPORTING_AREA', 'SHOOTING', 
               'UCR_PART', 'Location']
    crime = crime.drop(columns=del_col)
    
    # assuming each incident_number is assigned to individual offense
    # drop all the duplicates
    crime = crime.drop_duplicates(subset='INCIDENT_NUMBER')
    
    # sort df based on lat, then long, then street name
    crime = crime.sort_values(by='Lat').sort_values(by='Long').sort_values(by='STREET')
    
    # drop col without a lat, long, and location
    crime = crime.dropna(how='all', subset=['Lat', 'Long', 'STREET'])
    crime = crime.dropna(how='any', subset=['Lat', 'Long'])

    # fill the missing values (lat & long) in csv df w/ average of neighboring points 
    # using interpolation
    crime['Lat'] = crime['Lat'].interpolate()
    crime['Long'] = crime['Long'].interpolate()
    
    # change date-time col to just date
    date_series = pd.Series(crime["OCCURRED_ON_DATE"])
    
    # Convert the Series to pandas datetime type
    date_series = pd.to_datetime(date_series, format="%Y-%m-%d %H:%M:%S")

    # Extract only the date component
    crime["OCCURRED_ON_DATE"] = date_series.dt.date
    
    return crime


# In[3]:


def df_merged(df1, df2, df3):
    """merges three dataframe using full merge
    
    Args:
        df1, df2, df3 (dataframe): input dataframe
    
    Returns:
        DataFrame: a merged dataframe
    """
    combined_df = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

    return combined_df


# In[4]:


# read the csv file
crime_2018 = read_file('boston_crime_2018.csv')
crime_2020 = read_file('boston_crime_2020.csv')
crime_2022 = read_file('boston_crime_2022.csv')

# merge all to form one df
merged_df = df_merged(crime_2018, crime_2020, crime_2022)


# In[5]:


# show crime 2018 dataframe
crime_2018


# In[6]:


# show crime 2020 dataframe
crime_2020


# In[7]:


# show crime 2022b dataframe
crime_2022


# ### Creating new dataframe

# In[8]:


# create list of years
year = [2018, 2020, 2022]

# create dic to store all crime counts
m_counts = {}
d_counts = {}

# interate thru each year
for y in year:
    # filter years:
    specific_y = merged_df[merged_df['YEAR']==y] 
    
    # count crime in each month
    counts = specific_y['MONTH'].value_counts()
    counts = counts.sort_index()
    # add to dict
    m_counts[y] = counts
    
    # count crime in each day
    num = specific_y['DAY_OF_WEEK'].value_counts()
    num = num.sort_index()
    # add to dict
    d_counts[y] = num
    
    
# create dataframe for crime count per month
m_crime = pd.DataFrame(m_counts)
m_crime = m_crime.rename_axis('month')

# create dataframe for crime count per day of week
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]
d_crime = pd.DataFrame(d_counts)
d_crime = d_crime.reindex(index=day_order)
d_crime = d_crime.rename_axis('day of week')


# In[9]:


# new dataframe for monthly crimes
m_crime


# In[10]:


# new dataframe for weekly count crimes
d_crime


# In[11]:


# create new col = total case
d_crime['total'] = d_crime.sum(axis=1)
d_crime['total'] = d_crime['total'].round(0).astype(int)
d_crime


# ## Graphs

# ### Bar Graphs

# In[12]:


def bar(df):
    """ create bar graph of num of crime per month
    
    Args:
        df: cvs file 
        
    Return:
        bar plot
    
    """
    # create empty dic to store crime counts   
    count = {}
    
    # loop over each month 
    for i in range(1,13):
        # initiate the dic key & values
        count[i] = 0
        for months in df.MONTH:
            # add up the # of reported crime per month
            if months == i:
                count[i] += 1

    # set up color palette
    sns.set_palette('Set2')
    
    # plot the bar chart
    for key, value in count.items():
        plt.bar(key, value)

    # Set the x-axis label, y-axis label, xticks
    plt.xlabel('Month')
    plt.ylabel('Crime Rate')
    plt.xticks(range(1,13))
    plt.grid(alpha=0.3)

    # Show the plot
    plt.show()


# In[13]:


# plot merged df
plt.title('Total number of crime per month (2018-2022)')
bar(merged_df)


# ### Interactive bar graphs

# In[14]:


# month/year
# make a list of years we want to plot
yr = [2018, 2020, 2022]

# iterate thru yr and plot using the m_crime df
for i in yr:
    fig = px.bar(data_frame=m_crime, x=m_crime.index, y=i, color=m_crime.index)
    
    # edit the hover_data
    fig.update_traces(hovertemplate='Month: %{x}<br>Count: %{y}')
    
    # add title
    fig.update_layout(title = (f'Crime Count per Month in {i}'), 
                      xaxis_title='Months', yaxis_title='Crime Count')

    fig.show()


# In[15]:


# day of week
# make a list of years we want to plot
yr = [2018, 2020, 2022]

# iterate thru yr and plot using the m_crime df
for i in yr:
    fig = px.bar(data_frame=d_crime, x=d_crime.index, y=i, color=d_crime.index)
    
    # edit the hover_data
    fig.update_traces(hovertemplate='Day: %{x}<br>Count: %{y}')
    
    # add title
    fig.update_layout(title = (f'Crime Count For Each Day of Week in {i}'), 
                      xaxis_title='Day of Week', yaxis_title='Crime Count')

    fig.show()


# ## Line graph to compare years & months

# In[16]:


def line(df1, df2, df3):
    """
    Graph a line plot showing the crime rate per month for multiple dataframes
    
    Args:
        df1, df2, df3: Dataframes representing different datasets
    
    Returns:
        line plot
    """
    # create list of df
    year_df = [df1, df2, df3]
    
    # create list of corresponding years to df
    years = [2018, 2020, 2022]

    # iterate thru years & df
    for i in range(len(year_df)):
        df = year_df[i]
        year = years[i]

        # create empty dictionary to store crime counts
        count = {}

        # loop over each month
        for i in range(1, 13):
            # Initialize the dictionary key-value 
            count[i] = 0

        # count the number of reported crimes per month
        for month in df['MONTH']:
            count[month] += 1

        # extract the month and count data
        x = list(count.keys())
        y = list(count.values())

        # plot the line chart
        plt.plot(x, y, label=str(year))

    # set the x-axis label, y-axis label, and x-ticks
    plt.legend()
    plt.xlabel('Month')
    plt.ylabel('Crime Count')
    plt.xticks(range(1, 13))
    plt.title('Crime Counts Comparison (2018-2022)')
    plt.grid()

    # Show the plot
    plt.show()



# In[17]:


# plot line graph
line(crime_2018, crime_2020, crime_2022)


# ### Heatmap - show density

# In[18]:


def heatmap(df, y):
    """ heatmap of the crime locations
    
    Args: 
        df: dataframe of chosen csv
        y (int): year
        
    Return:
        heatmap
    """
    
    # initalize array
    crime_map = np.zeros((1000, 1000), dtype=int)

    # Define the bounds of the map (given from hw 1 about boston)
    max_lat = 42.4
    min_lat = 42.2
    
    max_lon = -71.2
    min_lon = -70.9

    # Iterate over the rows 
    for index, row in df.iterrows():
        # Get the latitude and longitude from the dataset
        lat = row['Lat']
        lon = row['Long']

        # the coordinates are within the defined bounds
        i = 1000 - int((lat - min_lat) / (max_lat - min_lat) * 1000)
        j = int((lon - min_lon) / (max_lon - min_lon)*1000)
        if i < 1000 and j < 1000:
        
            # increment count
            crime_map[i, j] += 1

    
    # Plot the heatmap
    plt.figure(dpi=600)
    plt.imshow(crime_map, cmap='plasma', vmax=1, alpha=1, origin='lower')
    plt.title(f'Crime Map {y}')
    plt.colorbar(label=f'crime percentage', cmap='plasma')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.xlim(200,1000)
    plt.ylim(0, 900)
    plt.grid(alpha=0.2)
    plt.show()
    


# In[19]:


heatmap(crime_2018, 2018)


# In[20]:


heatmap(crime_2020, 2020)


# In[21]:


heatmap(crime_2022, 2022)


# ## interactive heat map

# In[22]:


# 2018 crime
# find center of boston (coordinate from google)
boston_loc=[42.3601, -71.0589]

# Create the map
boston = folium.Map(location=boston_loc, zoom_start=11.65)

# Prepare data for HeatMap
df_map_2018 = merged_df[merged_df['YEAR'] == 2018][['Lat', 'Long']].values.tolist()

# Create a colormap for the heatmap
colormap = LinearColormap(['green', 'yellow', 'red'], vmin=0, vmax=1)

# Add heatmap layer to the map
HeatMap(df_map_2018, gradient={0.2: 'green', 0.5: 'yellow', 1: 'red'}, 
        min_opacity=4, radius=7, blur=15).add_to(boston)

# Add the color legend to the map
colormap.caption = 'Crime Occurance'
boston.add_child(colormap)

# Add a title to the map
folium.map.LayerControl('topright', title='Crime Heatmap').add_to(boston)

# Display the map with the heatmap
boston


# In[23]:


# 2020 crime
# find center of boston (coordinate from google)
boston_loc=[42.3601, -71.0589]

# Create the map
boston = folium.Map(location=boston_loc, zoom_start=11.65)

# Prepare data for HeatMap
df_map_2020 = merged_df[merged_df['YEAR'] == 2020][['Lat', 'Long']].values.tolist()

# Create a colormap for the heatmap
colormap = LinearColormap(['green', 'yellow', 'red'], vmin=0, vmax=1)

# Add heatmap layer to the map
HeatMap(df_map_2020, gradient={0.2: 'green', 0.5: 'yellow', 1: 'red'}, 
        min_opacity=4, radius=7, blur=15).add_to(boston)

# Add the color legend to the map
colormap.caption = 'Crime Occurance'
boston.add_child(colormap)

# Add a title to the map
folium.map.LayerControl('topright', title='Crime Heatmap').add_to(boston)

# Display the map with the heatmap
boston


# In[32]:


# heatmap for 2022
# find center of boston (coordinate from google)
boston_loc=[42.3601, -71.0589]

# Create the map
boston = folium.Map(location=boston_loc, zoom_start=11.65)

# Prepare data for HeatMap
df_map_2022 = merged_df[merged_df['YEAR'] == 2022][['Lat', 'Long']].values.tolist()

# Create a colormap for the heatmap
colormap = LinearColormap(['green', 'yellow', 'red'], vmin=0, vmax=1)

# Add heatmap layer to the map
HeatMap(df_map_2022, gradient={0.2: 'green', 0.5: 'yellow', 1: 'red'}, 
        min_opacity=4, radius=7, blur=15).add_to(boston)

# Add the color legend to the map
colormap.caption = 'Crime Occurance'
boston.add_child(colormap)

# Add a title to the map
folium.map.LayerControl('topright', title='Crime Heatmap').add_to(boston)

# Display the map with the heatmap
boston


# ### Pie chart

# In[33]:


# find the total crime of each year & put it to list
m_total = m_crime.sum().values.tolist()

# list of label
labels = [2018, 2020, 2022]
color = ['plum', 'mediumpurple', 'palevioletred']


plt.pie(m_total, labels=labels, colors = color, autopct='%1.1f%%')
plt.title('Percentage of Crime Rate')
plt.legend(loc ='upper left')
plt.show()


# In[34]:


# plot pie
fig = px.pie(data_frame=d_crime, names=d_crime.index, values='total', color=d_crime.index)

# Edit the hover_data
fig.update_traces(hovertemplate='Day: %{label}<br>Count: %{value}')

# Add title
fig.update_layout(title=f'Crime Precentage For Each Day of Week from 2018-2022',
                  xaxis_title='Day of Week', yaxis_title='Total Crime Count')

fig.show()


# ### Histogram

# In[35]:


def hist(df, year):
    """plot a histogram
    Args:
        df: dataframe
    """
    # filter out col = hours and put into a list
    df_hour = df['HOUR'].values.tolist()
    
    # plot
    plt.hist(df_hour, bins=24, edgecolor='black', color='plum')
    
    # label
    plt.title(f'Crime Time Occurance {year}')
    plt.xlim(0,24)
    plt.xticks(range(0,24))
    plt.xlabel('Crime Time (Military Hours)')
    plt.ylabel('Crime Counts')
    plt.grid(alpha=0.2)
    plt.show()


# In[36]:


# histogram of 2018-2022
hist(merged_df, "2018-2022")


# In[38]:


# histogram of 2018
hist(crime_2018, 2018)


# In[39]:


# histogram of 2020
hist(crime_2020, 2020)


# In[40]:


# histogram of 2022
hist(crime_2022, 2022)

