import dash_cytoscape as cyto
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import utils

filtres_tab = dcc.Tab(label='Filtres', value = 'onglet1', children=[
                html.Div([
                    html.Div([
                        html.Label('Niveau'),
                        dcc.Checklist(
                            id='checklist-Niveau',
                            options=[{'label': i, 'value': i} for i in utils.niveau_options],
                            value=utils.niveau_options,  # Par défaut tout est sélectionné
                        ),
                    ], style={'grid-column': '1', 'grid-row': '1'} ),



                    #DOMAINES PRINCIPAUX


                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine_principal_1',
                            options=[{'label': i, 'value': i} for i in utils.domaine_principal_options_1],
                            value= utils.domaine_principal_options_1,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ], style={'grid-column': '2', 'grid-row': '2'} ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine_principal_2',
                            options=[{'label': i, 'value': i} for i in utils.domaine_principal_options_2],
                            value= utils.domaine_principal_options_2,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ], style={'grid-column': '3', 'grid-row': '2'} ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine_principal_3',
                            options=[{'label': i, 'value': i} for i in utils.domaine_principal_options_3],
                            value= utils.domaine_principal_options_3,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ], style={'grid-column': '4', 'grid-row': '2'} ),



                    #DOMAINE

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine1',
                            options=[{'label': i, 'value': i} for i in utils.domaine_options_1],
                            value= utils.domaine_options_1,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '2', 'grid-row': '3'} ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine2',
                            options=[{'label': i, 'value': i} for i in utils.domaine_options_2],
                            value= utils.domaine_options_2,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '3', 'grid-row': '3'} ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Domaine3',
                            options=[{'label': i, 'value': i} for i in utils.domaine_options_3],
                            value= utils.domaine_options_3,
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '4', 'grid-row': '3'} ),


                    #POLES

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Pole1',
                            options=[{'label': 'Produire', 'value': 'Produire'}],
                            value=['Produire'],
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '2', 'grid-row': '1'}  ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Pole2',
                            options=[{'label': 'Utiliser', 'value': 'Utiliser'}],
                            value=['Utiliser'],
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '3', 'grid-row': '1'}  ),

                    html.Div([
                        dcc.Checklist(
                            id='checklist-Pole3',
                            options=[{'label': 'Déployer', 'value': 'Déployer'}],
                            value=['Déployer'],
                            labelStyle={"display": "flex", "align-items": "center"},
                        ),
                    ],style={'grid-column': '4', 'grid-row': '1'}  ),



                    html.Div([
                        html.Label('Nature'),
                        dcc.Checklist(
                            id='checklist-Nature',
                            options=[{'label': i, 'value': i} for i in utils.nature_options],
                            value=utils.nature_options,
                        ),
                    ], ),



                    html.Div([
                        html.Label('Doublon'),
                        dcc.Checklist(
                            id='checklist-Doublon',
                            options=[{'label': i, 'value': i} for i in utils.doublon_options],
                            value=utils.doublon_options,
                        ),
                    ], style={'grid-column': '1', 'grid-row': '3'}),
                ],style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'gap': '20px'})
            ])