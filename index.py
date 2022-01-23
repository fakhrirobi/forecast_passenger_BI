from importlib import reload
import dash 
import dash_bootstrap_components as dbc 

from dash import html,Input,Output,State,dcc
from app import app,server


from apps import predictive_analytics,project_explanation,stats,api_docs
from apps.predictive_analytics import * 
from apps.project_explanation import *
from apps.stats import *
import apps.api_docs as api_docs
from apps.api_docs import * 





server = server
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#3083ff",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'background-color' : '#f0f3f7'

}

sidebar = html.Div(
    [
        html.H4("Choose Menu Below : "),
        dbc.Nav(
            [   dbc.NavLink("Project Explanation", href="/", active="exact"),
                dbc.NavLink("Statistics", href="/stats", active="exact"),
                dbc.NavLink("Predictive Analytics", href="/analytics", active="exact"),
                dbc.NavLink("API", href="/api", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page(pathname) : 
    if pathname == '/' : 
        project_explanation.layout = render_project_explanation()
        return project_explanation.layout

    elif pathname == '/stats' : 
        stats.layout = stats.render_statistics()
        return stats.layout
    elif pathname == '/analytics' : 
        predictive_analytics.layout = predictive_analytics.render_predictive_analytics_page()
        return predictive_analytics.layout
        
    elif pathname == '/api' : 
        api_docs.layout  = api_docs.render_api_docs()
        return api_docs.layout
    else : 
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
if __name__ == '__main__' : 
    
    app.run_server(debug=True,port=5555)