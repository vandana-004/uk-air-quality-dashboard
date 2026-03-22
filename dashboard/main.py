import dash
from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('UK Air Quality Dashboard'),
    # components will be imported here as they are merged
])

if __name__ == '__main__':
    app.run(debug=True)
