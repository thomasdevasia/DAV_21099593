import pandas as pd
import json
from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)

# reading the data from json file
file = open('./laureate.json')
data = json.load(file)['laureates']
file.close()

# making it into a dataframe
data = pd.DataFrame(data)

firstname = []
surname = []
bornCountryCode = []
diedCountryCode = []
gender = []
prizeYear = []
prizeCategory = []

for i,item in data.iterrows():
    for j in item['prizes']:
        firstname.append(item['firstname'])
        surname.append(item['surname'])
        bornCountryCode.append(item['bornCountryCode'])
        diedCountryCode.append(item['diedCountryCode'])
        gender.append(item['gender'])
        prizeYear.append(j['year'])
        prizeCategory.append(j['category'])

df = pd.DataFrame({
    'firstname':firstname,
    'surname':surname,
    'bornCountryCode':bornCountryCode,
    'diedCountryCode':diedCountryCode,
    'gender':gender,
    'prizeYear':prizeYear,
    'prizeCategory':prizeCategory
})

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    ''')
])



if __name__ == '__main__':
    
    app.run_server(debug=True)


    
