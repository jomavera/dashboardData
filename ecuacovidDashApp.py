import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )
server = app.server

#---------------------------------------------------------------
df = pd.read_csv("ecuacovid.csv")
df = df.rename(columns={"created_at": "date"})
available_indicators = list(df.columns)
df['ts'] = pd.to_datetime(df['date'],dayfirst=True)
min_date = df['ts'].min()
max_date = df['ts'].max()


mrkd_text = '''
Data taken from [source](https://github.com/andrab/ecuacovid/tree/master/datos_crudos) on 01/04/2021
'''


#---------------------------------------------------------------
app.layout = html.Div([
    html.H2([
        'Dashboard for COVID-19 data in Ecuador'
    ],style={'text-align':'center'}),
    html.Div([
        dcc.Markdown(children=mrkd_text)
    ],style={'text-align':'left'}),
    html.Div([
            html.H6(
                'Select time series:',
                style={'text-align':'left'}),
            dcc.Dropdown(
                id='crossfilter-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='muertes_confirmadas'
            ),
            html.H6(
                'Select y-axis type:',
                style={'text-align':'left'}),
            dcc.RadioItems(
                id='crossfilter-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'},
                style={'text-align':'left'}
            ),
            html.H6(
                'Select date range:',
                style={'text-align':'left'}),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                initial_visible_month=datetime(2020,6,15),
                start_date=min_date,
                end_date=max_date,
                style={'text-align':'left'}
            )
        ]
    ),
    html.Div([
        dcc.Graph(id='x-time-series')
        ],
        style={'width': '80%', 'height':'80%', 'margin-left': '5%'}
    )
],
className='container')

#------------------------------------------------------------------
def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='date', y=title, template='ggplot2')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-column', 'value'),
     dash.dependencies.Input('crossfilter-type', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_x_timeseries(column_name, axis_type, start_date, end_date):

    dff = df.loc[:,['ts', 'date', column_name] ]
    print(start_date)
    print(end_date)
    dff = dff.loc[(dff['ts']> start_date ) & ( dff['ts']< end_date ), :]
    print(dff[['ts','date']])
    return create_time_series(dff, axis_type, column_name)


# #------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)