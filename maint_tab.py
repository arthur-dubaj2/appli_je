import dash_cytoscape as cyto
from dash import dash_table
from dash import html
from dash import dcc
import utils
from legende import legende

# Styles modernes pour l'ensemble de l'onglet
main_container_style = {
    'width': '100%',
    'minHeight': '100vh',
    'background': 'linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%)',
    'padding': '20px',
    'fontFamily': "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
}

graph_container_style = {
    'backgroundColor': 'white',
    'borderRadius': '20px',
    'boxShadow': '0 10px 40px rgba(0, 0, 0, 0.1)',
    'padding': '20px',
    'marginBottom': '20px',
    'border': '1px solid rgba(0, 0, 0, 0.05)',
    'position': 'relative',
    'overflow': 'hidden'
}

# Style amélioré pour le graphe Cytoscape - Hauteur réduite
cytoscape_style = {
    'width': '100%',
    'height': '850px',
    'backgroundColor': '#fafbfc',
    'borderRadius': '15px',
    'border': '2px solid #e1e4e8'
}

# Style pour l'info-bulle
tooltip_style = {
    'position': 'absolute',
    'backgroundColor': 'rgba(44, 62, 80, 0.95)',
    'color': 'white',
    'padding': '12px 16px',
    'borderRadius': '10px',
    'boxShadow': '0 8px 24px rgba(0, 0, 0, 0.25)',
    'fontSize': '14px',
    'fontWeight': '500',
    'zIndex': 1000,
    'display': 'none',
    'pointerEvents': 'none',
    'backdropFilter': 'blur(8px)',
    'border': '1px solid rgba(255, 255, 255, 0.1)',
    'maxWidth': '300px',
    'transition': 'all 0.2s ease'
}

# Style pour la table
table_container_style = {
    'backgroundColor': 'white',
    'borderRadius': '15px',
    'padding': '25px',
    'boxShadow': '0 8px 30px rgba(0, 0, 0, 0.08)',
    'marginBottom': '25px',
    'border': '1px solid rgba(0, 0, 0, 0.05)'
}

table_style = {
    'maxHeight': '400px',
    'overflowY': 'auto',
    'borderRadius': '10px',
    'border': '1px solid #e1e4e8'
}

table_cell_style = {
    'textAlign': 'left',
    'padding': '12px 15px',
    'fontFamily': "'Inter', sans-serif",
    'fontSize': '13px',
    'whiteSpace': 'normal',
    'lineHeight': '1.5'
}

table_header_style = {
    'backgroundColor': '#f6f8fa',
    'fontWeight': '700',
    'border': '1px solid #e1e4e8',
    'textTransform': 'uppercase',
    'fontSize': '12px',
    'letterSpacing': '0.5px',
    'color': '#2c3e50',
    'padding': '15px'
}

table_data_style = {
    'border': '1px solid #e1e4e8',
    'backgroundColor': 'white',
    'transition': 'background-color 0.2s ease'
}

# Style pour le formulaire d'ajout
form_container_style = {
    'backgroundColor': 'white',
    'padding': '30px',
    'borderRadius': '20px',
    'boxShadow': '0 10px 40px rgba(0, 0, 0, 0.08)',
    'marginBottom': '25px',
    'border': '1px solid rgba(0, 0, 0, 0.05)'
}

form_title_style = {
    'marginBottom': '25px',
    'color': '#2c3e50',
    'fontSize': '24px',
    'fontWeight': '700',
    'borderBottom': '3px solid #3498db',
    'paddingBottom': '15px',
    'letterSpacing': '0.5px'
}

input_style = {
    'margin': '10px',
    'padding': '12px 16px',
    'borderRadius': '10px',
    'border': '2px solid #e1e4e8',
    'width': '220px',
    'fontSize': '14px',
    'transition': 'all 0.3s ease',
    'fontFamily': "'Inter', sans-serif"
}

dropdown_style = {
    'margin': '10px',
    'width': '220px',
    'fontSize': '14px',
    'borderRadius': '10px'
}

button_style = {
    'background': 'linear-gradient(135deg, #88c000 0%, #03a3ff 100%)',
    'color': 'white',
    'padding': '12px 28px',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '600',
    'marginTop': '20px',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 2px 8px rgba(136, 192, 0, 0.3)',
    'letterSpacing': '0.5px',
    'textTransform': 'uppercase'
}

button_pole = {
    'background': '#f8f9fa',
    'color': 'black',
    'padding': '12px 28px',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '18px',
    'fontWeight': '600',
    'marginTop': '20px',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 2px 8px rgba(136, 192, 0, 0.3)',
    'letterSpacing': '0.5px',
    'textTransform': 'uppercase',
    'margin' : '0 20px'
}

#Style pour le bouton d'export excel

export_container_style = {
    'backgroundColor': 'white',
    'padding': '80px',
    'borderRadius': '20px',
    'boxShadow': '0 10px 40px rgba(0, 0, 0, 0.08)',
    'border': '1px solid rgba(0, 0, 0, 0.05)',
    'margin' : 'auto'
}

button_export = {
    
    'background': '#f8f9fa',
    'color': 'black',
    'padding': '12px 28px',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '18px',
    'fontWeight': '600',
    'marginTop': '20px',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 2px 8px rgba(136, 192, 0, 0.3)',
    'letterSpacing': '0.5px',
    'textTransform': 'uppercase',
    'margin' : '0 20px'
}


main_tab = dcc.Tab(
    label='Graphe et données',
    value='onglet2',
    style={
        'padding': '12px 24px',
        'fontWeight': '600',
        'fontSize': '15px'
    },
    selected_style={
        'padding': '12px 24px',
        'fontWeight': '700',
        'fontSize': '15px',
        'borderTop': '3px solid #3498db',
        'backgroundColor': '#f8f9fa'
    },
    children=[
        html.Div([
            

            # Conteneur principal : Graphe + Légende
            html.Div([
                html.Div([
                    # Buttons to choose pole
                    html.Div([
                        html.Button('Pôle Production', id='btn-pole-produire', n_clicks=0,
                                    style=button_pole),
                        html.Button('Pôle Déploiement', id='btn-pole-deployer', n_clicks=0,
                                    style=button_pole),
                        html.Button('Pôle Utilisation', id='btn-pole-utiliser', n_clicks=0,
                                    style=button_pole)
                    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '12px'}),

                    # store to keep current selected pole
                    dcc.Store(id='selected-pole'),

                    # Single Cytoscape that will be filtered by the store value
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=[e for e in utils.nodes + utils.edges],  # default full set; callback will replace
                        layout={'name': 'preset'},
                        style=cytoscape_style,
                        tapNodeData={'id': 'id'},
                        stylesheet=utils.generate_stylesheet(utils.df_nodes, 0)
                    ),
                ], style={**graph_container_style, 'flex': '1', 'marginRight': '20px'}),

                # Légende
                legende,
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'flex-start',
                'marginBottom': '30px'
            }),

            # Table des caractéristiques
            html.Div([
                html.H3('Détails de l\'organisation sélectionnée', style={
                    'color': '#2c3e50',
                    'fontSize': '22px',
                    'fontWeight': '700',
                    'marginBottom': '20px',
                    'letterSpacing': '0.5px'
                }),
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': i, 'id': i} for i in utils.df.columns[0:11]],
                    data=[],
                    style_table=table_style,
                    style_cell=table_cell_style,
                    style_header=table_header_style,
                    style_data=table_data_style,
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        },
                        {
                            'if': {'state': 'active'},
                            'backgroundColor': 'rgba(52, 152, 219, 0.1)',
                            'border': '1px solid #3498db'
                        }
                    ],
                    page_size=10
                ),
            ], style=table_container_style),

            # Formulaire d'ajout de nœud + bouton d'export
            html.Div([
                html.Div([
                    html.H3('Ajouter une nouvelle organisation', style=form_title_style),
                    html.Div([
                        dcc.Input(
                            id='node-nom',
                            placeholder='Nom de l\'organisation',
                            style=input_style
                        ),
                        dcc.Dropdown(
                            searchable=False,
                            id='node-niveau',
                            options=[{'label': n, 'value': n} for n in utils.df['Niveau'].unique()],
                            placeholder='Niveau',
                            style=dropdown_style
                        ),
                        dcc.Dropdown(
                            searchable=False,
                            id='node-pole',
                            options=[{'label': n, 'value': n} for n in utils.df['Pole'].unique()],
                            placeholder='Pôle',
                            style=dropdown_style
                        ),
                        dcc.Dropdown(
                            id='node-domaine_principal',
                            options=[{'label': n, 'value': n} for n in utils.df['Domaine_principal'].unique()],
                            placeholder='Domaine principal',
                            style=dropdown_style
                        ),
                        dcc.Dropdown(
                            id='node-domaine',
                            options=[{'label': n, 'value': n} for n in utils.df['Domaine'].unique()],
                            placeholder='Domaine',
                            style={**dropdown_style, 'width': '300px'}
                        ),
                        dcc.Dropdown(
                            searchable=False,
                            id='node-nature',
                            options=[{'label': n, 'value': n} for n in utils.df['Nature'].unique()],
                            placeholder='Nature',
                            style=dropdown_style
                        ),
                    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'marginBottom': '15px'}),
                    html.Div([
                        dcc.Dropdown(
                            searchable=False,
                            id='node-influence',
                            options=[{'label': n, 'value': n} for n in utils.df['Influence'].unique()],
                            placeholder='Influence',
                            style=dropdown_style
                        ),
                        dcc.Dropdown(
                            searchable=False,
                            id='node-interaction',
                            options=[{'label': n, 'value': n} for n in utils.df['Interaction'].unique()],
                            placeholder='Interaction',
                            style=dropdown_style
                        ),
                        dcc.Dropdown(
                            searchable=False,
                            id='node-doublon',
                            options=[{'label': n, 'value': n} for n in utils.df['Doublon'].unique()],
                            placeholder='Doublon',
                            style=dropdown_style
                        ),
                        dcc.Input(
                            id='node-acronyme',
                            placeholder='Acronyme',
                            style=input_style
                        ),
                    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
                    html.Button(
                        'Ajouter l\'organisation',
                        id='add-node-btn',
                        style=button_style,
                        className='add-button'
                    ),
                ], style=form_container_style),
                html.Div(
                    [html.Img(src='/assets/logo_xlsx.png', id = 'logo_excel', style={'width': '80px', 'marginBottom': '10px', 'margin' : 'auto', 'display' : 'block'}),
                    html.Div([html.Button("Download xlsx", id="btn_xslx", style = button_export), dcc.Download(id="download_xslx")])], style=export_container_style
                ),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ], style=main_container_style)
    ])
