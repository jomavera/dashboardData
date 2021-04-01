import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------
df = pd.read_csv("ecuacovid.csv")

available_indicators = list(df.columns)

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
            dcc.Dropdown(
                id='crossfilter-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='muertes_confirmadas'
            ),
            dcc.RadioItems(
                id='crossfilter-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
            ],
            style={'width': '100%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(id='x-time-series')
        ],
        style={'display': 'inline-block', 'width': '100%'}
    )
])

#------------------------------------------------------------------

def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='created_at', y=title)

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-column', 'value'),
     dash.dependencies.Input('crossfilter-type', 'value')])
def update_x_timeseries(column_name, axis_type):

    dff = df.loc[:,['created_at', column_name] ]
    return create_time_series(dff, axis_type, column_name)


# #------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)