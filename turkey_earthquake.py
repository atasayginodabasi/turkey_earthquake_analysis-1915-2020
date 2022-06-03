import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import re

# 1915-2021, greater than 3.5

# LAZIM OLUR (Belirli iki string arasındaki değerleri almaca)
'''''''''
start = '('
end = ')'

Yer = []
for y in range(len(data)):
    Yer.append("")

for i in range(0, len(data)):
    Yer[i] = data['Yer'][i]

    if Yer[i].find('(') != -1:
        Yer[i] = Yer[i][Yer[i].find(start) + len(start):Yer[i].rfind(end)]

Yer = pd.DataFrame(Yer)
Yer = Yer[0].str.split('[').str[0]
'''''''''

print(os.listdir(r'C:/Users/ata-d/'))
data = pd.read_csv(r'C:/Users/ata-d/OneDrive/Masaüstü/ML/Datasets/turkey_earthquakes(1915-2021).csv', delimiter=';')

data = data.drop(['No', 'Deprem Kodu', 'Tip'], axis=1)

# Splitting the dataframe due to before and after the '.'
data['Olus zamani'] = data['Olus zamani'].str.split('.').str[0]

# Saniye is greater than 60 for some data points. I located and dropped them
for i in range(0, len(data)):
    if float(data['Olus zamani'][i][6:]) >= 60:
        data = data.drop(i)
data = data.reset_index(drop=True)

# Creating single column for date and time
olus_zamani = pd.to_datetime(data['Olus tarihi'] + ' ' + data['Olus zamani'])
data['Olus zamani'] = olus_zamani
data.drop(['Olus tarihi'], axis=1, inplace=True)

# ----------------------------------------------------------------------------------------------------------------------

# Creating a list with empty string values
Yer = []
for y in range(len(data)):
    Yer.append("")

# Placing Yer values to the empty list
for i in range(0, len(data)):
    Yer[i] = data['Yer'][i]

    # If the Yer values have '(', it will divided by left and right side of the '(', ')' in order
    if Yer[i].find("(") != -1:
        Yer[i] = Yer[i].split('(')[1]
        Yer[i] = Yer[i].split(')')[0]
Yer = pd.DataFrame(Yer)

# Getting rid of the string values start with '['
Yer = Yer[0].str.split('[').str[0].to_frame()
Yer.columns = ['Yer']

# Placing the created Yer column to the original dataset
data['Yer'] = Yer

# Some data points have missing letters due to Turkish Alphabet unique letters
Yer_update = {"?ORUM": "CORUM", "K?TAHYA": "KUTAHYA", "EGE DENiZi": "EGE DENIZI",
              "DiYARBAKIR": "DIYARBAKIR", "T?RKiYE-iRAN SINIR B?LGESi": "TURKIYE-IRAN SINIR BOLGESI",
              "BALIKESiR ": "BALIKESIR", "SiVAS": "SIVAS", "iZMiR": "IZMIR", "TUNCELi": "TUNCELI",
              "SURiYE": "SURIYE", "ESKiSEHiR": "ESKISEHIR", "DENiZLi": "DENIZLI", "BiTLiS": "BITLIS",
              "KiLiS": "KILIS", "VAN G?L?": "VAN GOLU", "?ANKIRI": "CANKIRI",
              "T?RKIYE-IRAN SINIR B?LGESI": "TURKIYE-IRAN SINIR BOLGESI", "MANiSA": "MANISA",
              "AKDENiZ": "AKDENIZ", "G?RCiSTAN": "GURCISTAN", "BiNGOL": "BINGOL", "OSMANiYE": "OSMANIYE",
              "KIRSEHiR": "KIRSEHIR", "MARMARA DENiZi": "MARMARA DENIZI", "ERZiNCAN": "ERZINCAN",
              "BALIKESiR": "BALIKESIR", "GAZiANTEP": "GAZIANTEP", "G?RCISTAN": "GURCISTAN",
              "?ANAKKALE'": "CANAKKALE", "HAKKARi": "HAKKARI", "AFYONKARAHiSAR": "AFYONKARAHISAR",
              "BiLECiK": "BILECIK", "KAYSERi": "KAYSERI", "T?RKiYE-IRAK SINIR B?LGESi": "TURKIYE-IRAK SINIR BOLGESI",
              "KARADENiZ": "KARADENIZ", "T?RKIYE-IRAK SINIR B?LGESI": "TURKIYE-IRAK SINIR BOLGESI",
              "KARAB?K": "KARABUK", "KIBRIS-SADRAZAMK?Y?K": "KIBRIS-SADRAZAMKOY",
              "T?RKIYE-SURIYE SINIR B?LGESI?K": "TURKIYE-SURIYE SINIR BOLGESI", "?ANAKKALE": "CANAKKALE",
              "KIBRIS-SADRAZAMK?Y": "KIBRIS-SADRAZAMKOY", "ERZURUM ": "ERZURUM",
              "T?RKIYE-SURIYE SINIR B?LGESI": "TURKIYE-SURIYE SINIR BOLGESI", "ADANA ": "ADANA", "KUS G?L?": "KUS GOLU",
              "BURDUR ": "BURDUR", "KIBRIS-G?ZELYURT": "KIBRIS-GUZELYURT", "KONYA ": "KONYA",
              "KOCAELI ": "KOCAELI", "AMASYA ": "AMASYA", "KIRSEHIR ": "KIRSEHIR",
              "KIBRIS-KILI?ASLAN": "KIBRIS-KILICASLAN", "KIBRIS-Z?MR?TK?Y": "KIBRIS-ZUMRUTKOY",
              "DENIZLI ": "DENIZLI", "MANISA ": "MANISA", "ULUBAT G?L?": "ULUBAT GOLU",
              "T?RKIYE-ERMENISTAN SINIR B?LGESI": "TURKIYE-ERMENISTAN SINIR BOLGESI",
              "ERZINCAN ": "ERZINCAN", "TOKAT ": "TOKAT", "ARDAHAN ": "ARDAHAN"}
data['Yer'] = data['Yer'].replace(Yer_update)

# ----------------------------------------------------------------------------------------------------------------------

# Number of Earthquakes Annually
'''''''''
aa = data['Olus zamani'].value_counts()
aa = aa.resample('Y').sum().to_frame()
fig = px.line(aa, x=aa.index, y='Olus zamani', text='Olus zamani',
              labels={
                  "index": "Year",
                  "Olus zamani": "Number of Earthquakes"
              }
              )
fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig.update_traces(textposition='top center')
fig.update_layout(title_text='Number of Earthquakes Annually',
                  title_x=0.5, title_font=dict(size=30))
fig.show()
'''''''''

# Distribution of the Earthquakes (Annually)
'''''''''
fig_hist = px.histogram(data_frame=data, x='Olus zamani')
fig_hist.update_layout(title_text='Distribution of the Earthquakes (Annually)',
                       title_x=0.5, title_font=dict(size=32))
fig_hist.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig_hist.show()
'''''''''

# Distribution of the Magnitudes
'''''''''
fig = px.histogram(data, x="xM", marginal='rug', hover_data=data.columns)
fig.update_layout(title_text='Distribution of the Magnitudes',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
'''''''''

# Distribution of the Depth(km)
'''''''''
fig = px.histogram(data, x="Derinlik", marginal='rug', hover_data=data.columns)
fig.update_layout(title_text='Distribution of the Depth(km)',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
'''''''''

# Number of Earthquakes due to Location
'''''''''
Yer_count = data.groupby(pd.Grouper(key='Yer')).size().reset_index(name='count')
fig = px.treemap(Yer_count, path=['Yer'], values='count')
fig.update_layout(title_text='Number of Earthquakes due to Location',
                  title_x=0.5, title_font=dict(size=30)
                  )
fig.update_traces(textinfo="label+value")
fig.show()
'''''''''

# Top 10 Frequent Earthquake Locations
'''''''''
Yer_count = data.groupby(pd.Grouper(key='Yer')).size().reset_index(name='count')
Yer_count_top = Yer_count.nlargest(10, 'count')[['Yer', 'count']]
fig = px.bar(Yer_count_top, x='Yer', y='count', color='Yer', text='count')
fig.update_layout(title_text='Top 10 Frequent Earthquake Locations',
                  title_x=0.5, title_font=dict(size=30))
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()
'''''''''

# Heatmap of the Earthquakes (animated)
'''''''''
fig = px.density_mapbox(data, lat=data['Enlem'], lon=data['Boylam'], z=data['xM'],
                        center=dict(lat=38.087369, lon=32.077329), zoom=5.5,
                        mapbox_style="stamen-terrain",
                        radius=15,
                        opacity=0.5,
                        animation_frame=pd.DatetimeIndex(data['Olus zamani']).year)
fig.update_layout(title_text='Heatmap of the Earthquakes',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
'''''''''

# Heatmap of the Earthquakes (stable)
'''''''''
fig = px.density_mapbox(data, lat=data['Enlem'], lon=data['Boylam'], z=data['xM'],
                        center=dict(lat=38.087369, lon=32.077329), zoom=5.5,
                        mapbox_style="stamen-terrain",
                        radius=10,
                        opacity=0.5)
fig.update_layout(title_text='Heatmap of the Earthquakes',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
'''''''''

# Top 30 Largest Earthquakes in the Turkey
'''''''''
top_mag = data.nlargest(30, 'xM')[['Yer', 'xM', 'Enlem', 'Boylam']]
fig = px.density_mapbox(top_mag, lat=top_mag['Enlem'], lon=top_mag['Boylam'], z=top_mag['xM'],
                        center=dict(lat=38.087369, lon=32.077329), zoom=5.5,
                        mapbox_style="open-street-map",
                        radius=30,
                        opacity=0.8)
fig.update_layout(title_text='Top 30 Largest Earthquakes in the Turkey',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
'''''''''

# Top 30 Earthquakes due to Magnitude vs Year
'''''''''
fig = px.scatter(data.nlargest(30, 'xM')[['xM', 'Yer', 'Olus zamani']],
                 x='Olus zamani', y='xM', color='Yer', text='xM', hover_name='Olus zamani',
                 size='xM')
fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(title_text='Top 30 Earthquakes due to Magnitude vs Year',  # Main title for the project
                  title_x=0.5, title_font=dict(size=30))  # Location and the font size of the main title

fig.show()
'''''''''

# Correlation Graph
'''''''''
plt.figure(figsize=(15, 8))
correlation = sns.heatmap(data.corr(), vmin=-1, vmax=1, annot=True, linewidths=1, linecolor='black')
correlation.set_title('Correlation Graph of the Dataset', fontdict={'fontsize': 24})
'''''''''

# Distribution of the Earthquakes due to Lat and Long (M>5) *******
'''''''''
fig = go.Figure(data=[go.Scatter3d(
    x=data['Enlem'],
    y=data['Boylam'],
    z=data[data['xM'] >= 5]['xM'],
    mode='markers+text',
    hovertext=data['Yer'],
    marker=dict(
        size=5,
        color=data['xM'],
        colorscale='Viridis',
        opacity=0.8
    ),
    text=data[data['xM'] >= 5]['xM'],
)])
fig.update_layout(scene=dict(
    xaxis_title='Latitude',
    yaxis_title='Longitude',
    zaxis_title='xM')
)
fig.update_layout(title_text='Distribution of the Earthquakes due to Lat and Long (M>5)',
                  title_x=0.5, title_font=dict(size=22))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.show()
'''''''''

# The Relationship between the Depth and the Magnitude
fig = px.scatter(data, x='xM', y='Derinlik')
fig.update_layout(title='The Relationship between the Depth and the Magnitude', title_x=0.5, title_font=dict(size=30))
fig.show()
