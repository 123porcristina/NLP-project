import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
from Code import main
import pandas as pd
from pathlib import Path

dir_base = (str(Path(__file__).parents[1]) + '/Data')
df_file = pd.read_pickle(dir_base + "/df_data.pickle")
df_tokens = pd.read_pickle(dir_base + "/df_tokens.pickle")
del df_tokens['speech']
df_tokens['token_speech'] = df_tokens['token_speech'].astype('str')


app = dash.Dash(__name__)
app.css.append_css({'external_url': 'static/custom.css'})
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    # HEADER
    html.Div(
        id='header-div',
        className='header',
        children=[
            html.Img(src='/assets/nlc.jpg'),
            html.H2('Natural Language Processing - Topic Identification'),
        ]),

################### START DCC TABS ###################
    html.Div(
        id='div-dcc',
        className='div-dcc-container',
        children=[
            dcc.Tabs(id='dcc-tabs',
                     parent_className='custom-tabs',
                     className='custom-tabs-container',
                     children=[
################### START DCC TABS  - ABOUT ###################
                         dcc.Tab(label='About',
                                 value='tab-1',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.H4(className='H4-text', children='Overview'),
                                     html.P(className='P-text', children=
                                     'The purpose of this project is to use '
                                     'Natural Language Processing (NLP) techniques '
                                     'to analyze mayor’s speeches from cities around '
                                     'the United States to identify local policy '
                                     'trends. The goal would be to use topic modeling '
                                     'to identify policy topics in speeches. '
                                     ''
                                     'The dataset '
                                     'consists of about 150 speeches per year and is '
                                     'between the years 2016-2019. The first objective '
                                     'would be to create a topic model to represent the '
                                     'distribution of topics across the full dataset. '
                                     ''
                                     'Once the overall distribution of policy topics is obtained, '
                                     'it will be further segmented by year, region, and population '
                                     'to analyze the similarities and differences in the '
                                     'distribution of the topics.')
                                 ]),

################### START DCC TABS  - UPLOAD DATA ###################
                         dcc.Tab(label='Upload Data',
                                 value='tab-2',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(
                                         id='file-upload-container',
                                         title='Upload your own dataset here.',
                                         children=[
                                             dcc.Upload(
                                                 id='file-upload',
                                                 className='control-upload',
                                                 children=html.Div([
                                                     "Drag and drop files, or click \
                                                                to select files."
                                                 ]),
                                                 multiple=True
                                             ), ], ),

                                     html.Div(
                                         'Select a loaded dataset',
                                         title='Choose a pre-loaded dataset',
                                         className='loaded-dataset-text',
                                     ),

                                     dcc.Dropdown(
                                         id='dropdown-datasets',
                                         className='control-upload-dropdown',
                                         options=[
                                             {'label': str((row['city'] + ', ' + row['state'] + ' - ' + row['year'])),
                                              'value': str((row['city'] + ',' + row['state'] + '-' + row['year']))}
                                             for index, row in df_file.iterrows()
                                         ],
                                         placeholder='Select a Dataset'
                                     ),  # End Dropddown

                                     html.Div(
                                         id='div-load-button',
                                         className='div-preprocess-button',
                                         children=[
                                             html.Button(id='button-load-data',
                                                            n_clicks=0,
                                                            children='Convert files to a Dataset',
                                                            className='button-preprocess'),
                                            ])
                                 ]),

################### START DCC TABS  - PREPROCESSING ###################
                         dcc.Tab(label='Preprocessing',
                                 value='tab-3',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(
                                         id='div-text-radio-items-1',
                                         className='div-text-radio-items',
                                         children=[
                                     html.P(id='text_radio-items-1',
                                            className='text_radio-items',
                                            children=['Add Regions to the dataset?']),

                                     dcc.RadioItems(id='radio-items-1',
                                                    className='radio-items',
                                                     options=[
                                                     {'label':'yes', 'value':'yes'},
                                                     {'label': 'no', 'value': 'no'},
                                                 ]),
                                    ]),
                                     html.Div(
                                         id='div-text-radio-items-2',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text_radio-items-2',
                                                className='text_radio-items',
                                                children=['Remove Stopwords?']),

                                             dcc.RadioItems(id='radio-items-2',
                                                            className='radio-items',
                                                            options=[
                                                                {'label': 'yes', 'value': 'yes'},
                                                                {'label': 'no', 'value': 'no'},
                                                            ]),
                                            ]),
                                     html.Div(
                                         id='div-text-radio-items-3',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text_radio-items-3',
                                                    className='text_radio-items',
                                                    children=['Remove Entities?']),

                                             dcc.RadioItems(id='radio-items-3',
                                                            className='radio-items',
                                                            options=[
                                                                {'label': 'yes', 'value': 'yes'},
                                                                {'label': 'no', 'value': 'no'},
                                                            ]),
                                        html.Div(
                                            id='div-preprocess-button',
                                            className='div-preprocess-button',
                                            children=[
                                                html.Button('Run Preprocessing',
                                                            id='button-preprocess',
                                                            n_clicks=0,
                                                            className='button-preprocess'),
                                                html.Button('Reset Preprocessing',
                                                            id='button-reset',
                                                            n_clicks=0,
                                                            className='button-preprocess')
                                        ])
                                         ]),
                                 ]),  # End Tab PREPROCESSING

################### START DCC TABS  - LDA MODEL ###################
                         dcc.Tab(label='LDA Model',
                                 value='tab-4',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.H4(className='H4-text', children='TAB 4'),

                                 ]),
                     ]),
        ]),

################### START TABLES / RIGHTS DIVS  ###################
    html.Div(id='container-tabs'),  # Right Div - Speeches
    html.Div(id='table-upload-data'), # Table -dataset before preprocess
    html.Div(id='table-preprocess-data')  # Table -dataset before preprocess

]) # End App Layout Div


################################################################################
###
### CALLBACKS
###
################################################################################

#FUNCTION TAB 2 - SHOW TABLE BEFORE PREPROCESS

# CALLBACK TO UPDATE CONTENT DEPENDING ON THE TAB YOU'RE IN
@app.callback(Output('table-upload-data', 'children'),
              [Input('dcc-tabs', 'value')])
def display_content(selected_tab):
    if selected_tab == 'tab-2':
        return html.Div(id='div-right-table')


#FUNCTION TAB 2 - CALLBACK BUTTON SHOW TABLE BEFORE PREPROCESS
@app.callback(
    Output('div-right-table', 'children'),
    [Input('button-load-data', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks >= 1:
        return html.Div(id='div-upload-data',
                        className='div-table-upload',
                        children=[
                            html.H4(id='Speeches Dataset',
                                    className='title-speech-dataset',
                                    children='Table of Speeches'),
                            dt.DataTable(
                                id='table-preprocessing',
                                columns=[{"name": i, "id": i} for i in df_file.columns],
                                data=df_file.to_dict('records'),
                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'text-align': 'center'
                                    },
                                style_cell={
                                    'backgroundColor': 'rgb(35, 35, 35)',
                                    'color': 'white',
                                    'text-align': 'left',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'width': '100px'
                                },
                                fixed_rows={'headers': True, 'data': 0},
                                fixed_columns={'headers': True, 'data': 3},
                                style_table={'overflowX': 'scroll', 'minWidth': '100%'}
                            )
                        ])


###########################################



#CALLBACK BUTTON SHOW TABLE AFTER PREPROCESS
@app.callback(
    Output('div-right-preprocessing', 'children'),
    [Input('div-preprocess-button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks >= 1:
        return html.Div(id='div-table-preprocessing',
                        className='div-right-preprocessing',
                        children=[
                            html.H4(id='tokens-Dataset',
                                    className='title-speech-dataset',
                                    children='Table of Speeches Tokenized'),
                            dt.DataTable(
                                id='table-tokens',
                                columns=[{"name": str(i), "id": str(i)} for i in df_tokens.columns],
                                data=df_tokens.to_dict('records'),
                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'text-align': 'center'
                                    },
                                style_cell={
                                    'backgroundColor': 'rgb(35, 35, 35)',
                                    'color': 'white',
                                    'text-align': 'left',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'width': '100px'
                                },
                                fixed_rows={'headers': True, 'data': 0},
                                fixed_columns={'headers': True, 'data': 4},
                                style_table={'overflowX': 'scroll', 'minWidth': '100%'}
                            )
                                ])  # End Right Div - Table for tab 3

#FUNCTION TAB 2 - SHOW TABLE BEFORE PREPROCESS







# CALLBACK TO UPDATE CONTENT DEPENDING ON THE TAB YOU'RE IN
@app.callback(Output('container-tabs', 'children'),
              [Input('dcc-tabs', 'value')])
def display_content(selected_tab):
    if selected_tab == 'tab-2':
        return html.Div(id='div-right-speech',
                        className='div-right-speech',
                        children=[
                            html.H4(id='div-right-speech-title'),
                            html.P(id='div-right-speech-body')
                        ])  # End Right Div - Speeches

    elif selected_tab == 'tab-3':
        return html.Div(id='div-right-preprocessing')  # End Right Div - Table for tab 3






#####################################
# CALLBACK TO RETURN THE SPEECH TITLE
@app.callback(Output('div-right-speech-title', 'children'),
              [Input('dropdown-datasets', 'value')])
def output_dropdown(value):
    return html.H4(value)


# CALLBACK TO RETURN THE SPEECH TEXT
@app.callback(Output('div-right-speech-body', 'children'),
              [Input('dropdown-datasets', 'value')])
def output_dropdown(value):
    for index, row in df_file.iterrows():
        if value == str(row['city'] + ',' + row['state'] + '-' + row['year']):
            speech = row['speech']
    return html.P(speech)

################################################################################
###
### RUN
###
################################################################################
if __name__ == '__main__':
    app.run_server()
