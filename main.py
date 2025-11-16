import dash
from dash import html
from dash import dcc 
from dash.dependencies import Input, Output, State
import numpy as np
import dash_bootstrap_components as dbc
import utils
from filtres_tab import filtres_tab 
from maint_tab import main_tab
import pandas as pd
import os

# Initialisation de l'application Dash avec le thème Bootstrap et styles personnalisés
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # Le fichier CSS dans assets/ sera automatiquement chargé
)


server = app.server

# Définition du layout principal avec système d'onglets et stockage de données
app.layout = html.Div([
    # En-tête avec logo France Hydrogène
    html.Div([
        html.Div([
            html.Img(
                src='assets/logo_FH.jpg',
                style={
                    'height': '60px',
                    'marginRight': '20px'
                }
            ) if 'assets/logo_FH.jpg' else None,
            html.Div([
                html.H1("Who's wHy", style={
                    'margin': '0',
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'color': '#003a91',
                    'letterSpacing': '0.5px'
                }),
                html.P("Cartographie des parties prenantes de l'hydrogène", style={
                    'margin': '0',
                    'fontSize': '14px',
                    'color': '#666',
                    'fontWeight': '400'
                })
            ])
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'padding': '20px',
            'backgroundColor': 'white',
            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
            'borderRadius': '0 0 15px 15px'
        })
    ], style={'marginBottom': '20px'}),
    
    # Onglets
    dcc.Tabs(
        id='tabs',
        value='onglet1',
        children=[
            filtres_tab,
            main_tab
        ],
        style={
            'fontFamily': "'Roboto', sans-serif",
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
            'padding': '5px',
            'margin': '0 20px'
        },
        parent_style={
            'backgroundColor': 'transparent'
        }
    ),
    
    # Stockage des données
    dcc.Store(id='stored-tap-data'),
    dcc.Store(id='stored-elements'),
    dcc.Store(id='stored-data-table'),
    dcc.Store(id='zoom-flag', data=False)

], style={
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh',
    'paddingTop': '20px'
})

# Callback pour mettre à jour le pôle sélectionné

@app.callback(
    Output('selected-pole', 'data'),
    [Input('btn-pole-utiliser', 'n_clicks'),
     Input('btn-pole-deployer', 'n_clicks'),
     Input('btn-pole-produire', 'n_clicks')]
)
def set_selected_pole(n_innov, n_bus, n_ind):
    ctx = dash.callback_context

    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    mapping = {
        'btn-pole-utiliser': 'Utiliser',
        'btn-pole-deployer': 'Déployer',
        'btn-pole-produire': 'Produire',
        '' : 'Produire'
    }

    return mapping[btn]


# Callaback pour afficher le bouton correspondant au pôle sélectionné en surbrillance

@app.callback(
[Output('btn-pole-utiliser','className'),
Output('btn-pole-deployer','className'),
Output('btn-pole-produire','className')],
[Input('selected-pole','data')]
)

def highlight_pole(selected):
    base = 'pole-btn' # facultatif : classe de base si vous en avez
    c_utiliser = base + (' pole-selected' if selected == 'Utiliser' else '')
    c_deployer = base + (' pole-selected' if selected == 'Déployer' else '')
    c_produire = base + (' pole-selected' if selected == 'Produire' else '')
    return c_utiliser, c_deployer, c_produire


@app.callback(
    Output("download_xslx", "data"),
    [Input("btn_xslx", "n_clicks")],
    prevent_initial_call=True,
)
def generate_xlsx(n_nlicks):
    def to_xlsx(bytes_io):
        xslx_writer = pd.ExcelWriter(
            bytes_io, engine="xlsxwriter"
        )  # requires the xlsxwriter package
        utils.df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.close()

    return dcc.send_bytes(to_xlsx, "database.xlsx")

# Fonction principale de filtrage des données selon les critères sélectionnés
def filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole="Utiliser"):


    
    domaine_principal2 = [x for x in domaine_principal if utils.dico_placement[x] in poles]
    

    # Filtrer le dataframe en fonction des valeurs sélectionnées
    filtered_df = utils.df[
        (utils.df['Niveau'].isin(niveau)) &
        (utils.df['Domaine_principal'].isin(domaine_principal2)) &
        (utils.df['Domaine'].isin(domaine)) &
        (utils.df['Nature'].isin(nature)) &
        (utils.df['Doublon'].isin(doublon))&
        (utils.df['Pole'] == selected_pole)

    ]

    node_liste = list(np.concatenate((filtered_df['Nom'].values, utils.base_liste)))

    for dp in utils.domaine_principal_options:
        if utils.dico_placement[dp] not in poles or utils.dico_placement[dp] != selected_pole:
            node_liste.remove(dp)

    for pole in utils.poles:
        if pole != selected_pole:
            node_liste.remove(pole)

    node_liste = np.array(node_liste)


    # Filtrer les arêtes (edges) en fonction des nœuds filtrés
    filtered_edges = [edge for edge in utils.edges if
                    edge['data']['source'] in  node_liste and
                    edge['data']['target'] in node_liste]


    dico_nbr = {}
    for dom in domaine_principal:
        dico_nbr[dom] = 0
    dico_nbr['Généraliste '] = 0
    for n in node_liste:
        if n not in utils.base_liste:
            dom = (utils.df).loc[(utils.df)['Nom'] == n, 'Domaine_principal'].iloc[0]
            dico_nbr[dom] += 1

    # Créer les éléments du graphe pour Cytoscape
    elements = filtered_edges + [
        {
            'data': {'id': node, 'label': node},
            'position' : utils.position(node, dico_nbr),
            'classes': 'node-class'
        }
        for node in node_liste
    ]

    return elements, node_liste




#fonction appliquée dans le callback suivant pour appliquer le "zoom" avec la fonction genere_sous_graphe

def callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole="Utiliser"):
    elements, node_liste =   filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
    elements2 = utils.genere_sous_graphe(data['id'], node_liste, domaine)
    return elements2



"""@app.callback(
    Output('stored-tap-data', 'data'),
    Input('cytoscape', 'tapNodeData')
)
def update_store(tap_node_data):
    print("update store flag")
    if tap_node_data:
        return tap_node_data  # Stocker les données du nœud cliqué
    return None  # Réinitialiser si aucune interaction"""

@app.callback(
    Output('stored-tap-data', 'data'),
    [Input('cytoscape', 'tapNodeData')],
    [State('stored-tap-data', 'data')]
)
def update_store(tap_node_data, current_data):


    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger == 'add-node-btn':
        return None  # Réinitialiser stored_data quand on ajoute un nœud
    elif tap_node_data:
        return tap_node_data
    return current_data





@app.callback(
    [Output('cytoscape', 'elements'),
    Output('table', 'data'),
    Output('cytoscape', 'layout'),
    Output('stored-tap-data', 'clear_data'),
    Output('cytoscape', 'stylesheet'),
    Output('stored-elements', 'data'),
    Output('stored-data-table', 'data'),
    Output('zoom-flag', 'data')],
    
    [Input('tabs', 'value'),
    Input('checklist-Niveau', 'value'),
    Input('checklist-Domaine_principal_1', 'value'),
    Input('checklist-Domaine_principal_2', 'value'),
    Input('checklist-Domaine_principal_3', 'value'),
    Input('checklist-Domaine1', 'value'),
    Input('checklist-Domaine2', 'value'),
    Input('checklist-Domaine3', 'value'),
    Input('checklist-Pole1', 'value'),
    Input('checklist-Pole2', 'value'),
    Input('checklist-Pole3', 'value'),
    Input('checklist-Nature', 'value'),
    Input('checklist-Doublon', 'value'),
    Input('cytoscape', 'layout'),
    Input('stored-tap-data', 'data'),
    Input('stored-elements', 'data'),
    Input('stored-data-table', 'data'),
    Input('zoom-flag', 'data'),
    Input('add-node-btn', 'n_clicks'), 
    Input('selected-pole', 'data')
    ],
    [State('node-nom', 'value'),
    State('node-niveau', 'value'),
    State('node-pole', 'value'),
    State('node-domaine_principal', 'value'),
    State('node-domaine', 'value'),
    State('node-nature', 'value'),
    State('node-influence', 'value'),
    State('node-interaction', 'value'),
    State('node-doublon', 'value'),
    State('node-acronyme', 'value'),
    State('cytoscape', 'elements')]
)


def update_cytoscape_table(tab,niveau, domaine_principal1,  domaine_principal2,  domaine_principal3, domaine1 , domaine2, domaine3, poles1, poles2, poles3, nature, doublon,
                        layout, stored_data,stored_elements,data_table,zoom_flag, n_clicks, selected_pole,nom, niveau_val, pole_val, dp_val, domaine_val, nature_val, influence_val, interaction_val, doublon_val, acronyme_val,
                        elements):
    


    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    

    domaine = domaine1 + domaine2 + domaine3
    domaine_principal = domaine_principal1 + domaine_principal2 + domaine_principal3
    poles = poles1 + poles2 + poles3

    table_data = data_table

    stored_data_clean = False
    edges_width = 0
    data = stored_elements




    if stored_data and (trigger != "add-node-btn" and tab == "onglet2"):

        
        if stored_data['id'] in utils.domaine_principal_options :
            if not(zoom_flag):
                elements = callback_sous_graphe(stored_data, niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
                edges_width = 0.5
                zoom_flag = True
            else:
                elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
                zoom_flag = False
                stored_data_clean = True

        # Mise à jour des données pour la table

            

            return elements, table_data, layout, stored_data_clean, utils.generate_stylesheet(utils.df_nodes, edges_width), stored_data, data_table, zoom_flag
        
        else:

            stored_data_clean = True
            if zoom_flag:
                elements = callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
                edges_width = 0.5
            else:
                elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
            node_id = stored_data['id']
            table_data = utils.df[utils.df['Nom'] == node_id].iloc[:, :11].to_dict('records')
            return elements, table_data, layout, stored_data_clean, utils.generate_stylesheet( utils.df_nodes, edges_width),  stored_elements, table_data, zoom_flag



    
    

    # Ajouter un nœud si le bouton est cliqué
    if trigger == 'add-node-btn':

        # Créer un nouveau nœud
        new_node = {
            'data': {'id': nom, 'label': nom},
            'classes': 'node-class'
        }

        # Ajouter le nœud à la liste d'éléments
        elements.append(new_node)

        
        # Ajouter le nœud au dataframe
        new_row = {
            'Nom': nom,
            'Acronyme': acronyme_val,
            'Niveau': niveau_val,
            'Pole': pole_val,
            'Domaine_principal': dp_val,
            'Domaine': domaine_val,
            'Nature': nature_val,
            'Influence': int(influence_val),
            'Interaction': int(interaction_val),
            'Doublon': doublon_val,
            'Commentaires': '',
            'Site': '',
            1: np.nan,
            2: np.nan
        }
        try:
            utils.df.loc[len(utils.df)] = new_row
            print("réussite ajout au DataFrame")
        except Exception as e:
            print("Erreur lors de l'ajout au DataFrame :", e)
            print("new_row keys:", new_row.keys())
            print("df columns:", utils.df.columns) 

        print("Nouveau nœud ajouté au dataframe :", new_row)

        shape = utils.forme_dico[niveau_val]
        couleur = utils.couleur_dico[nature_val]
        taille = int(influence_val) * 8
        acronyme = acronyme_val

        if doublon_val == "Doublon positif":
            l_color = 'rgb(0,255,0)'
        elif doublon_val == "Doublon négatif":
            l_color = 'rgb(255,0,0)'
        else:
            l_color = 'rgb(0,0,0)'

        if influence_val != 'nan':
            label_size = str(int(influence_val) * 3 + 10)
        else:
            label_size = 15

        ligne = [ shape, couleur, taille, acronyme, l_color, label_size, nom]
        utils.df_nodes.loc[len(utils.df_nodes)] = ligne

        if zoom_flag:
            elements = callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
            edges_width = 0.5
        else:
            elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)

        

        return elements, table_data, layout, True, utils.generate_stylesheet(utils.df_nodes, edges_width), stored_elements, data_table, zoom_flag


    if zoom_flag:
        elements = callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)
        edges_width = 0.5
    else:
        elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon, selected_pole)


    
    return elements, table_data, layout, True, utils.generate_stylesheet(utils.df_nodes, edges_width), stored_elements, data_table, zoom_flag
# Dépendances dans les filtres selon la hiérarchie
@app.callback(
    [Output('checklist-Domaine_principal_1', 'value'),
     Output('checklist-Domaine_principal_2', 'value'),
     Output('checklist-Domaine_principal_3', 'value'),
     Output('checklist-Domaine1', 'value'),
     Output('checklist-Domaine2', 'value'),
     Output('checklist-Domaine3', 'value')],
    [Input('checklist-Pole1', 'value'),
     Input('checklist-Pole2', 'value'),
     Input('checklist-Pole3', 'value'),
     Input('checklist-Domaine_principal_1', 'value'),
     Input('checklist-Domaine_principal_2', 'value'),
     Input('checklist-Domaine_principal_3', 'value')]
)
def update_all_domains(pole1, pole2, pole3, dp1_current, dp2_current, dp3_current):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Mise à jour des domaines principaux basée sur les pôles
    
    
    # Si le trigger vient des pôles, on met à jour aussi les domaines
    if trigger_id in ['checklist-Pole1', 'checklist-Pole2', 'checklist-Pole3']:

        dp1 = utils.domaine_principal_options_1 if 'Produire' in (pole1 or []) else []
        dp2 = utils.domaine_principal_options_2 if 'Utiliser' in (pole2 or []) else []
        dp3 = utils.domaine_principal_options_3 if 'Déployer' in (pole3 or []) else []

        domaines1 = []
        domaines2 = []
        domaines3 = []
        
        for dp in dp1:
            domaines1.extend(utils.dico_sous_graphe[dp])
        for dp in dp2:
            domaines2.extend(utils.dico_sous_graphe[dp])
        for dp in dp3:
            domaines3.extend(utils.dico_sous_graphe[dp])
    # Sinon on met à jour les domaines basés sur les domaines principaux actuels
    else:

        dp1 = dp1_current
        dp2 = dp2_current
        dp3 = dp3_current


        domaines1 = []
        domaines2 = []
        domaines3 = []
        
        for dp in (dp1 or []):
            domaines1.extend(utils.dico_sous_graphe[dp])
        for dp in (dp2 or []):
            domaines2.extend(utils.dico_sous_graphe[dp])
        for dp in (dp3 or []):
            domaines3.extend(utils.dico_sous_graphe[dp])

            
    return dp1, dp2, dp3, domaines1, domaines2, domaines3

if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 8051))
    #app.run_server(host="0.0.0.0", port=port, debug=False)
    app.run(debug=True, port = 8051)



