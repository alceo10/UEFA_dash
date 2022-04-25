import pandas as pd
import dash
from dash import html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

wd = r'C:\Users\pedro\Desktop\Cool Data'
file_name = r'\UEFA_Club.csv'

app = dash.Dash()   #initialising dash app
uefa_df = pd.read_csv(wd + file_name, sep = ';') #reading marathon dataset

top10_df = uefa_df.sort_values(by='total', ascending=False).loc[:9]
top10_clubs = list(set(top10_df['club']))
clubs =  list(set(uefa_df['club']))
nations =  ['all'] + sorted(list(set(uefa_df['country'])))

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'UEFA RANKING BY CLUB', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
        
        dcc.Dropdown( id = 'year',
        options = ['total','2022','2021','2020','2019','2018'],
        value = 'total'),
        
        
        dcc.Dropdown( id = 'club',
        options = clubs,
        value = top10_clubs,
        multi = True),
        
        dcc.Dropdown( id = 'nation',
        options = nations,
        value = ['all'],
        multi = True),
        
        dcc.Graph(id='bar_plot', figure=go.Figure())
                
    ])


@app.callback(Output('bar_plot','figure'),
              [Input('year', 'value'),
              Input('club', 'value'),
              Input('nation', 'value')])
    

def graph_update(input_year, input_club, input_nation):
    
    def usable_df(df):
        if input_nation != ['all']:
            sliced_df = uefa_df.loc[uefa_df['country'].isin(input_nation)]
        else:
            sliced_df = uefa_df.loc[uefa_df['club'].isin(input_club)]
            
        return sliced_df
    
    print(input_nation)
    
    df = usable_df(uefa_df)  
    
    fig = px.bar(df, x = 'club', y = '{}'.format(input_year))
    
    fig.update_layout(title = '',
                  xaxis_title = 'Club',
                  yaxis_title = 'UEFA Coefficient')
    
    fig.update_xaxes(categoryorder='total ascending')
    fig.show()

    return fig
    
if __name__ == '__main__': 
    app.run_server()
    
    