import dash_bootstrap_components as dbc
from flask import Flask
import dash

server = Flask(__name__)
server.config['DEBUG'] = True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname='/')

from NLP_package import routes