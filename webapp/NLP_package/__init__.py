from flask import Flask
import dash

server = Flask(__name__)
server.config['DEBUG'] = True
app = dash.Dash(__name__, server=server, url_base_pathname='/home/')

from NLP_package import routes