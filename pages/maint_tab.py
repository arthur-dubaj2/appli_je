import dash_cytoscape as cyto
from dash import dash_table
from dash import html
from dash import dcc
import utils
from legende import legende

main_tab = dcc.Tab(label='Graphe et données', value = 'onglet2', children=[
                html.Div([

                    #Graphe

                    cyto.Cytoscape(
                            id='cytoscape',
                            elements = utils.nodes + utils.edges,
                            layout={
                                'name': 'preset'},
                            style={'width': '80%', 'height': '600px', 'display': 'inline-block'}
                        ,tapNodeData={'id': 'id'},
                            stylesheet=utils.generate_stylesheet(utils.df_nodes, 0)
                    ),

                    #Etiquette affichant le nom du noeud en survol

                    html.Div(id='node-info', style={
                        'position': 'absolute', 'background-color': '#f1f1f1', 
                        'border': '1px solid black', 'padding': '5px', 
                        'display': 'none', 'zIndex': 10
                    }),

                    #Légende

                    legende,


                    #Table des caractéristiques des noeuds

                    dash_table.DataTable(
                        id='table',
                        columns=[{'name': i, 'id': i} for i in utils.df.columns[0:11]],
                        data=[],  # Initialisation vide
                        style_table={
                            'maxHeight': '300px',  # Limite la hauteur de la table
                            'overflowY': 'auto',  # Ajoute un défilement vertical
                            'border': '1px solid #ccc',
                            'margin-top': '20px',
                        },
                        style_cell={
                            'textAlign': 'left',  # Alignement du texte à gauche pour une meilleure lisibilité
                            'padding': '5px',
                            'font-family': 'Arial, sans-serif',
                            'font-size': '14px',
                            'whiteSpace' : 'normal',
                        },
                        style_header={
                            'backgroundColor': '#f2f2f2',
                            'fontWeight': 'bold',
                            'border': '1px solid #ddd',
                        },
                        style_data={
                            'border': '1px solid #ddd',
                        },
                    ),



                    #Outil d'ajout


                    html.Div([
                        html.Label('Ajouter un nouveau nœud'),
                        dcc.Input(id='node-nom', placeholder='Nom', style={'margin-right': '10px'}),
                        dcc.Input(id='node-niveau', placeholder='Niveau', style={'margin-right': '10px'}),
                        dcc.Input(id='node-domaine', placeholder='Domaine', style={'margin-right': '10px'}),
                        dcc.Input(id='node-nature', placeholder='Nature', style={'margin-right': '10px'}),
                        dcc.Input(id='node-influence', placeholder='Influence', style={'margin-right': '10px'}),
                        dcc.Input(id='node-interaction', placeholder='Interaction', style={'margin-right': '10px'}),
                        dcc.Input(id='node-doublon', placeholder='Doublon', style={'margin-right': '10px'}),
                        dcc.Input(id='node-acronyme', placeholder='Acronyme', style={'margin-right': '10px'}),
                        html.Button('Add Node', id='add-node-btn'),
                    ], style={'margin-top': '20px'})
                ])
            ])
