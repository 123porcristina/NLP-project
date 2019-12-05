import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from NLP_package import app
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import dash_table
import pandas as pd
from NLP_package.core import *
import os
import csv

from NLP_package.core import ReadText
from NLP_package.core import PreprocessingSpeech as ps
from NLP_package.core import Model
from pathlib import Path
import pandas as pd
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns',10)

###################################################
# Constants
###################################################

NAVBAR_LOGO = "https://kanchan-ghimire.s3.amazonaws.com/logo1.png"
UPLOAD_FOLDER = './uploads/'
CSV_FILENAME = 'df_tokens.csv'

###################################################
# Data
###################################################

###################################################
# TEMPORARY
###################################################

data = [
    {'name': "2016",
    'x': [0.86, 1.5, 2.2, 2.6, 2.7, 3, 3.67],
    'y': [6.40, 8.34, 9.46, 11.13, 12.55, 18.68],
    'type': "line"},
    {'name': "Manhattan",
    'x': [0.93, 1.33, 2.4, 2.6, 2.94, 3.34, 4.11],
    'y': [9.34, 10.09, 13.24, 16.53, 15.64, 25.65],
    'type': "line"}
]

TEMP = html.Div(children=[
    dcc.Graph(
        figure = {	
            'data': data,	
            'layout': {	
                'title': 'Here is a graph'	
            }	
        }	
    )
])


###################################################
# Components
###################################################

### Navbar

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=NAVBAR_LOGO, height="50px")),
                    dbc.Col(
                        dbc.NavbarBrand("NLP Project", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)


### Main Tab Components

UPLOAD_FILE = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': 'auto',
            'margin-top': '15px',
            'max-width': '80%'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

PRE_PROCESS_BUTTON = dbc.Button(
    "Pre-process File",
    id="pre-process-buton",
    color="info",
    block=True,
    style={
        'max-width': '50%',
        'margin': 'auto',
        'margin-top': '20px',
        'margin-bottom': '20px'
    }
    )

def generate_download_file_button(filename):
     return html.A(
        "Download Processed File",
        id="download-button",
        href='file',
        className='btn btn-info btn-block',
        style={
            'max-width': '50%',
            'margin': 'auto',
            'margin-top': '20px',
            'margin-bottom': '20px'
        }
    )

DOWNLOAD_FILE = dbc.Button(
    "Download Processed File",
    id="download-button-disabled",
    color="info",
    className='btn btn-info',
    block=True,
    style={
        'max-width': '50%',
        'margin': 'auto',
        'margin-top': '20px',
        'margin-bottom': '20px'
    }
    )


### Dashboard Tab Components

OPTIONS = dbc.Jumbotron(
    [
        html.H5('OPTIONS'),
        html.Hr(className="my-2"),
        dbc.Button('Generate Topics', id='generate-topics-button', style={'margin':'20px'}, block=True),
        dbc.RadioItems(
            options=[
                {'label': 'Option 1', 'value': 'Option 1'},
                {'label': 'Option 2', 'value': 'Option 2'},
                {'label': 'Option 3', 'value': 'Option 3'}
            ],
        value='MTL'
)  
    ],
    id='dashboard-options'
)
GRAPH_SIDE = dbc.Card(
    [
        dbc.CardHeader(html.H4("Bar Graph")),
        dbc.CardBody(
            [
                dcc.Graph(
                    figure = {	
                        'data': data,
                    }	
                )
            ]

        )
    ]
)

IFRAME = html.Iframe(
            src="/topic-graphic",
            height="100%",
            width='100%',
            style={
                'border-style':'none',
                'align':'middle',
                'margin':'auto'
            }
        )

GRAPH_LOWER = dbc.Card(
    [
        dbc.CardHeader(html.H4("Bar Graph")),
        dbc.CardBody(
            [
                dcc.Graph(
                    figure = {	
                        'data': data,
                    }	
                )
            ]

        )
    ]
)

### Body Tabs

MAIN_TAB = dbc.Col(
    [
        UPLOAD_FILE,
        PRE_PROCESS_BUTTON,
        html.Div(id="pre-processed"),
        html.Div([DOWNLOAD_FILE], id='download-file')
    ],
    id="main-tab"
)

DASHBOARD_TAB = html.Div(
        [
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col(OPTIONS, md=4, align='center'),
                        dbc.Col(GRAPH_SIDE, md=8),
                    ],
                    style={
                        'margin-top': '15px',
                    }
                ),
                    dbc.Row(
                        [
                            IFRAME
                        ],
                        style={
                            'margin':'0px',
                            'height':'1114px',
                            'width': '856',
                            'display':'block'
                        },
                    )
                ],
                style={
                    'max-width':'1250px'
                }
            )
        ],
        id="dashboard-tab"
)


### Main Body

BODY = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Main",
                    children=[DASHBOARD_TAB]
                    ),
                dcc.Tab(
                    label="Dashboard",
                    children=[MAIN_TAB]
                )
            ]
        )
    ],

    id="main-body"
)




###################################################
# App
###################################################

app.layout = html.Div(children=[NAVBAR, BODY])


###################################################
# Callbacks
###################################################

# Upload File

def save_to_csv(fname, filtered_list):
    with open(f'{UPLOAD_FOLDER}/{fname}', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(filtered_list)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    docx_path = 'Speeches 2020/DOC speeches'
    pdf_path = 'Speeches 2020/PDF speeches'

    file_path = f'{UPLOAD_FOLDER}/{filename}'

    with open(file_path, "wb") as fh:
        fh.write(base64.b64decode(content_string))

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            return "Cannot display or processs CSV file"

        elif 'xls' in filename:
            return "Cannot display or process Excel file"
        elif 'docx' in filename:
            docx_dir = f'{UPLOAD_FOLDER}/{docx_path}'

            with open(f'{docx_dir}/{filename}', "wb") as fh:
                fh.write(base64.b64decode(content_string))

            print('[INFO]...Reading')
            readText = ReadText.ReadDoc(docx_dir)
            df_files = readText.read_directory_files()
            name = 'df_data'
            save_df = ReadText.SaveDf(UPLOAD_FOLDER, df_files, name)
            save_df.save_dataframe()
            print('[INFO]...Loading Pickle')
            df = pd.read_pickle(UPLOAD_FOLDER+"/df_data.pickle")


        elif 'pdf' in filename:
            pdf_dir = f'{UPLOAD_FOLDER}/{pdf_path}'

            with open(f'{pdf_dir}/{filename}', "wb") as fh:
                fh.write(base64.b64decode(content_string))

            print('[INFO]...Reading')
            readText = ReadText.ReadDoc(pdf_dir)
            df_files = readText.read_directory_files()
            name = 'df_data'
            save_df = ReadText.SaveDf(UPLOAD_FOLDER, df_files, name)
            save_df.save_dataframe()
            print('[INFO]...Loading Pickle')
            df = pd.read_pickle(UPLOAD_FOLDER+"/df_data.pickle")            

        else:
            return html.Div([
                'Cannot display or process file'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing file(s).'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Region'},
                    'textAlign': 'left'
                }
            ]
        ),

        html.Hr(),
    ])


@app.callback([Output('output-data-upload', 'children'),
                Output('download-file', 'children')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    button = DOWNLOAD_FILE
    children = ''
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        button = generate_download_file_button('file')
    return children, button

@app.callback([Output('pre-processed', 'children')],[Input('pre-process-buton', 'n_clicks')])
def pre_process_files(x):
    if x is not None:
        print('[INFO]...Preprocessing')
        df_file = pd.read_pickle(UPLOAD_FOLDER+"/df_data.pickle")
        preprocessing = ps.Preprocessing(speeches=df_file)
        clean_tokens = preprocessing.clean_data()
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(clean_tokens)))
        print('[INFO]...Saving Pickle')
        name = 'df_tokens'
        save_df = ReadText.SaveDf(UPLOAD_FOLDER, clean_tokens, name)
        save_df.save_dataframe()
        print('[INFO]...Reading pickle tokens')
        df = pd.read_pickle(UPLOAD_FOLDER+"/df_tokens.pickle")

        save_to_csv(CSV_FILENAME, df.token_speech[0])

        return [html.Div([
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_cell={'textAlign': 'left'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Region'},
                        'textAlign': 'left'
                    }
                ]
            ),
            html.Hr(),
        ])]
    return [html.Div(id="pre-processed-data")]

@app.callback([],[])
def process_topic_graphic():
    return ''