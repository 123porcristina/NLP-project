import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
from pathlib import Path
from Code import ReadText
from Code import PreprocessingSpeech as ps
from Code import Model
from pathlib import Path
import pandas as pd

################################################################################
###
### IMPORT DATA
###
################################################################################
dir_base = (str(Path(__file__).parents[1]) + '/Data')

df_file = pd.read_pickle(dir_base + "/df_data.pickle")
df_tokens = pd.read_pickle(dir_base + "/df_tokens.pickle")
df_lda = pd.read_pickle(dir_base + "/df_lda.pickle")
del df_tokens['speech']
df_tokens['token_speech'] = df_tokens['token_speech'].astype('str')

################################################################################
###
### RUN MODEL
###
################################################################################

"""Model over the whole data"""
# model = Model.ModelTopic(doc=df_lda)
# bigram_speech, common_words = model.model_bigram()
# print(type(common_words))

# lda_result, coherence_lda = model.lda_model(num_topics=10, chunksize=100, alpha='auto', eta='auto', passes=300)  # change 100 for the vble in plotly
# print(coherence_lda)

# list_lda = []
# for idx, topic in lda_result.show_topics(num_topics=10, formatted=False, num_words=15):
#     print('Topic: {} \tWords: {}\n'.format(idx, '|'.join([w[0] for w in topic])))
#     list_lda.append(('Topic: {} \tWords: {}\n'.format(idx, '|'.join([w[0] for w in topic]))))
#
# lda_str = ''.join(list_lda)






# model.model_year()
# model.model_region()

################################################################################
###
### APP LAYOUT
###
################################################################################
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
                                            ]),

                                     html.Div(
                                         id='div-preprocess-button',
                                         className='div-preprocess-button',
                                         children=[
                                             html.Button('Run Preprocessing',
                                                         id='button-preprocess',
                                                         n_clicks=0,
                                                         className='button-preprocess-run'),
                                             html.Button('Reset Preprocessing',
                                                         id='button-reset',
                                                         n_clicks=0,
                                                         className='button-preprocess-run')
                                         ])
                                 ]),  # End Tab MODEL LDA


################### START DCC TABS  - LDA MODEL ###################
                         dcc.Tab(label='LDA Model',
                                 value='tab-4',
                                 className='custom-tab',
                                 selected_className='custom-tab--selected',
                                 children=[
                                     html.Div(
                                         id='div-text-num-topics',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text-num-topics',
                                                    className='text_radio-items',
                                                    children=['Number of topics: ']),

                                             dcc.Input(id='text-field-num-topics',
                                                       value=15,
                                                       type='number',
                                                       className='text-lda'),

                                         ]),
                                     html.Div(
                                         id='div-text-chunksize',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text-chunksize',
                                                    className='text_radio-items',
                                                    children=['Chunksize: ']),

                                             dcc.Input(id='text-field-chunksize',
                                                       value=100,
                                                       type='number',
                                                       className='text-lda'),
                                         ]),

                                     html.Div(
                                         id='div-text-alpha',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text-alpha:',
                                                    className='text_radio-items',
                                                    children=['Alpha: ']),

                                             dcc.Input(id='text-field-alpha',
                                                       value='auto',
                                                       type='text',
                                                       className='text-lda'),

                                            ]),

                                     html.Div(
                                         id='div-text-eta',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text-eta:',
                                                    className='text_radio-items',
                                                    children=['ETA: ']),

                                             dcc.Input(id='text-field-eta',
                                                       value='auto',
                                                       type='text',
                                                       className='text-lda'),


                                         ]),

                                     html.Div(
                                         id='div-text-passes',
                                         className='div-text-radio-items',
                                         children=[
                                             html.P(id='text-passes:',
                                                    className='text_radio-items',
                                                    children=['Passes: ']),

                                             dcc.Input(id='text-field-passes',
                                                       value='300',
                                                       type='number',
                                                       className='text-lda'),

                                         ]),

                                     html.Div(
                                         id='div-lda-button',
                                         className='div-preprocess-button-lda',
                                         children=[
                                             html.Button('Run LDA Model',
                                                         id='button-lda',
                                                         n_clicks=0,
                                                         className='button-lda'),
                                         ])
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
                                fixed_columns={'headers': True, 'data': 4},
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
                                fixed_columns={'headers': True, 'data': 5},
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
        return html.Div(id='div-right-preprocessing')  # End Right Div - Table for tab

    elif selected_tab == 'tab-4':
        return html.Div(id='div-right-lda')  # End Right Div - Table for tab 3


#RUN LDA MODEL - INPUT HYPERPARAMETERS LDA
@app.callback(Output('div-right-lda', 'children'),
              [Input('button-lda', 'n_clicks')],
              [State('text-field-num-topics', 'value'),
               State('text-field-chunksize', 'value'),
               State('text-field-alpha', 'value'),
               State('text-field-eta', 'value'),
               State('text-field-passes', 'value')])
def output(n_clicks, num_topics, chunksize, alpha, eta, passes):
    if n_clicks >= 1:
        model = Model.ModelTopic(doc=df_lda)
        bigram_speech, common_words = model.model_bigram()
        lda_result, coherence_lda, _, _ = model.lda_model(num_topics=int(num_topics),
                                                    chunksize=int(chunksize),
                                                    alpha=alpha,
                                                    eta=eta,
                                                    passes=int(passes))

        list_lda = []
        for idx, topic in lda_result.show_topics(num_topics=int(num_topics), formatted=False, num_words=15):
            list_lda.append(('Topic: {} \tWords: {}\n'.format(idx, '|'.join([w[0] for w in topic]))))

        lda_str = ''.join(list_lda)

        df_year = model.model_year()
        df_region = model.model_region()

        df_year_new = df_year.drop(columns='combined')
        df_region_new = df_region.drop(columns='combined')

        data_year = list()
        data_region =list()

        for i, row in df_year_new.iterrows():
            x_list = list()
            y_list = list()

            for lda_tuple in row['lda']:
                x_list.append(lda_tuple[0])
                y_list.append(lda_tuple[1])

            rows_dict = {'name': row['year'], 'x': x_list, 'y': y_list, 'mode': "markers",
                         'marker': {'size':  12}}
            data_year.append(rows_dict)

        for i, row in df_region_new.iterrows():
            x_list = list()
            y_list = list()

            for lda_tuple in row['lda']:
                x_list.append(lda_tuple[0])
                y_list.append(lda_tuple[1])

            rows_dict = {'name': row['Region'], 'x': x_list, 'y': y_list, 'mode': "markers",
                         'marker': {'size':  12}}
            data_region.append(rows_dict)

        return html.Div(id='content-lda',
                        className='div-lda',
                        children=[
                                html.Div(id='lda-text-result', className='lda-text-result',
                                         children=[
                                             html.H4(id='lda-result-title',
                                             className='lda-result-title',
                                             children=['LIST OF TOPICS']),

                                            html.Textarea(id='lda-text-area',
                                                          className='lda-text-area',
                                                          children=[lda_str]),
                                            html.H3(id='lda-accuracy',
                                                    className='lda-accuracy',
                                                    children=['Accuracy: ', f'{coherence_lda*100:.2f}', '%'])]
                                    ),
                                html.Div(id='div-lda-graphs',
                                         className='div-lda-graphs',
                                         children=[
                                             html.Iframe(
                                                 src=app.get_asset_url('lda.html'),
                                                 height="100%",
                                                 width='100%',
                                                 style={
                                                     'border-style': 'none',
                                                     'align': 'middle',
                                                     'margin': 'auto',
                                                     'background-color': 'darkgrey'
                                                 }
                                             )
                                            ],
                                            style={
                                                'max-width': '1250px',
                                                'height': '860px'
                                            }
                                    ),
                                dcc.Graph(
                                     figure={
                                         'data': data_year,
                                         'layout': {
                                             'title': 'Topic Distribution by Year',
                                             'plot_bgcolor': 'darkgrey',
                                             'paper_bgcolor': 'darkgrey',
                                             'xaxis':"Topic",
                                             'yaxis':"Probability"
                                         }
                                     },
                                    className='div-lda-graphs',
                                    style={
                                        'max-width': '1250px'
                                    }
                                 ),
                                dcc.Graph(
                                    figure={
                                        'data': data_region,
                                        'layout': {
                                            'title': 'Topic Distribution by Region',
                                            'plot_bgcolor': 'darkgrey',
                                            'paper_bgcolor': 'darkgrey',
                                            'xaxis':'Topic',
                                            'yaxis':'Probability'
                                        }
                                    },
                                    className='div-lda-graphs',
                                    style={
                                        'max-width': '1250px'
                                    }
                                )
                            ]
                        )




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
