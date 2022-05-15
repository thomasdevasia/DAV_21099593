# from turtle import tilt, title
from pydoc import classname
import pandas as pd
import json
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests

app = Dash(__name__)

# reading the data from json file for prize winners
file = open('./laureate.json')
laureates = json.load(file)['laureates']
file.close()

# reading the data from json file for country code
file = open('./country.json')
countries = json.load(file)['countries']
file.close()

# result = requests.get('https://api.nobelprize.org/v1/laureate.json')
# laureates = result.json()['laureates']

# result = requests.get('http://api.nobelprize.org/v1/country.json')
# country = result.json()


# making it into a dataframe
laureates = pd.DataFrame(laureates)
countries = pd.DataFrame(countries)

# converting to a datframe of required datas
name = []
country = []
diedCountry = []
gender = []
prizeYear = []
prizeCategory = []

for i,item in laureates.iterrows():
    for j in item['prizes']:
        if pd.isna(item['surname']) :
            name.append(item['firstname'])
        else:
            name.append(item['firstname']+' '+item['surname'])
        
        if pd.isna(item['bornCountryCode']):
            country.append('International')
        else:
            country.append(countries[countries['code'] == item['bornCountryCode']].name.iloc[0])

        gender.append(item['gender'])
        prizeYear.append(j['year'])
        prizeCategory.append(j['category'])

df = pd.DataFrame({
    'name':name,
    'country':country,
    'gender':gender,
    'prizeYear':prizeYear,
    'prizeCategory':prizeCategory
}).sort_values(by='prizeYear').reset_index(drop=True)

# adding count column to use scatter plot to make dot matrix plot
countArr = []
count = -1
temp = 0
for i in range(len(df)):
    if df['prizeYear'].iloc[i] != temp:
        count = -1
        temp = df['prizeYear'].iloc[i]

    count = count + 1
    countArr.append(count)
df['count'] = countArr

# scatter graph
scatter_fig = px.scatter(df, x='prizeYear', y='count', color='gender', hover_name='name')
scatter_fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Count",
    legend_title="Gender",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    )
)

# histogram graph
histogram_fig = px.histogram(df, x='prizeCategory', color='gender')
histogram_fig.update_layout(
    xaxis_title="Prize Category",
    yaxis_title="Count",
    legend_title="Gender",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    )
)

# preparing cummulative data
male = df[df['gender']=='male']
female = df[df['gender']=='female']
org = df[df['gender']=='org']

male =  male.groupby('prizeYear')['count'].count().reset_index()
maleYear = male['prizeYear']
maleCummSum = np.array(male['count']).cumsum()

female =  female.groupby('prizeYear')['count'].count().reset_index()
tempYear = []
tempCount = []
for i,item in male.iterrows():
    if len(female[female['prizeYear'] == item['prizeYear']]) == 0:
        tempYear.append(item['prizeYear'])
        tempCount.append(0)
    else:
        tempYear.append(female[female['prizeYear'] == item['prizeYear']].iloc[0]['prizeYear'])
        tempCount.append(female[female['prizeYear'] == item['prizeYear']].iloc[0]['count'])
female = pd.DataFrame({'prizeYear':tempYear, 'count':tempCount})
femaleYear = female['prizeYear']
femaleCummSum = np.array(female['count']).cumsum()

org =  org.groupby('prizeYear')['count'].count().reset_index()
tempYear = []
tempCount = []
for i,item in male.iterrows():
    if len(org[org['prizeYear'] == item['prizeYear']]) == 0:
        tempYear.append(item['prizeYear'])
        tempCount.append(0)
    else:
        tempYear.append(org[org['prizeYear'] == item['prizeYear']].iloc[0]['prizeYear'])
        tempCount.append(org[org['prizeYear'] == item['prizeYear']].iloc[0]['count'])
org = pd.DataFrame({'prizeYear':tempYear, 'count':tempCount})
orgYear = org['prizeYear']
orgCummSum = np.array(org['count']).cumsum()

# line graph
line_fig = go.Figure()
line_fig.add_trace(go.Scatter(x=maleYear, y=maleCummSum, name='Male'))
line_fig.add_trace(go.Scatter(x=femaleYear, y=femaleCummSum, name='Female'))
line_fig.add_trace(go.Scatter(x=orgYear, y=orgCummSum, name='Org'))

line_fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Count",
    legend_title="Gender",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    )
)


# default
tab1_fig = scatter_fig

# female percentage
fp = (len(df[df['gender']=='female'])/len(df))*100

app.layout = html.Div(children=[
    
    html.Div(className='heading',children=[
        html.H1(children='Noble Laueretes'),
        html.P(children='A Quick Look at Nobel Prize winners till now')
    ]),

    dcc.Tabs(id='tabGroup',children=[
        dcc.Tab(
            label='Over the Years',
            children=[
                html.Div(className='subHeading',children=[
                    html.H2(children='Winners over the Years based on Gender'),
                    html.P(children=[
                        html.Span(children='*'),
                        'Gender contains male, female or Organization'
                        ])
                ]),

                html.Div(className='insight',children=[
                    html.H4(children='Few Insights:'), 
                    html.Ul(children=[
                        html.Li(children=f'Only {str(fp)[:4]}% of winners are women!'),
                        html.Li(children='Marie Curie is the first woman to Nobel Prize'),
                        html.Li(children='Red cross is the only Organization to win Nobel Prize 3 times in 1917, 1944 and 1963')

                    ])
                    
                ]),

                html.Div(id='scatter-plot',children=[
                    dcc.Dropdown(['Normal','Cummulative'], 'Normal', id='tab1_dropDown'),
                    dcc.Graph(
                        id='tab1-grpah',
                        figure=tab1_fig
                    )
                ]),

            ]
        ),
        dcc.Tab(
            label='In different Categories',
            children=[
                html.Div(className='subHeading',children=[
                    html.H2(children='Winners in different Categories based on Gender'),
                    html.P(children=[
                        html.Span(children='*'),
                        'Gender contains male, female or Organization'
                        ])
                ]),

                html.Div(className='insight',children=[
                    html.H4(children='Few Insights:'), 
                    html.Ul(children=[
                        html.Li(children='The Physics and the Economics Prizes has only 2% women Winners.'),
                        html.Li(children='There are 224 Nobel Prize winners for Medicine')
                    ])
                    
                ]),

                dcc.Graph(
                    id='histogram-plot',
                    figure=histogram_fig
                )

            ]
        )
    ])
    
])



@app.callback(
    Output('tab1-grpah','figure'),
    Input('tab1_dropDown', 'value')
)
def updateGraph(value):
    if value == 'Normal':
        tab1_fig = scatter_fig
    else:
        tab1_fig = line_fig
    
    return tab1_fig



if __name__ == '__main__':
    
    app.run_server(debug=True, port=8050) 
    