import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import numpy as np
import dash_bootstrap_components as dbc
import utils
from filtres_tab import filtres_tab
from maint_tab import main_tab



# Initialiser l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Définir le layout de l'application
app.layout = html.Div([
    dcc.Tabs(
        id = 'tabs',
        value = 'onglet1',
        children = [
            filtres_tab,

            main_tab ]
    ),
    dcc.Store(id='stored-tap-data'),
    dcc.Store(id='stored-elements'),
    dcc.Store(id='stored-data-table'),
    dcc.Store(id = 'zoom-flag',data = False)

])

# Callbacks
#def register_callbacks(app):
@app.callback(
    Output('node-info', 'children'),
    Output('node-info', 'style'),
    Input('cytoscape', 'mouseoverNodeData')
)
def display_node_info(mouseover_data):
    if mouseover_data:
        node_label = mouseover_data['label']
        node_position = {'x': 0, 'y': 66}
        
        # Affiche les informations du nœud avec sa position
        return (
            f"Nom : {node_label}",
            {'display': 'block', 
            'position': 'absolute',
            'top': f'{node_position["y"]}px', 
            'left': f'{node_position["x"]}px',
            'background-color': '#f1f1f1', 'padding': '5px',
            'border': '1px solid black'}
        )
    else:
        return "", {'display': 'none'}


#Fonction gérant l'action des filtres, nécessaires dans les deux callbacks

def  filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon):

    
    domaine_principal2 = [x for x in domaine_principal if utils.dico_placement[x] in poles]
        

    # Filtrer le dataframe en fonction des valeurs sélectionnées
    filtered_df = utils.df[
        (utils.df['Niveau'].isin(niveau)) &
        (utils.df['Domaine_principal'].isin(domaine_principal2)) &
        (utils.df['Domaine'].isin(domaine)) &
        (utils.df['Nature'].isin(nature)) &
        (utils.df['Doublon'].isin(doublon))
    ]

    node_liste = list(np.concatenate((filtered_df['Nom'].values, utils.base_liste)))

    for dp in utils.domaine_principal_options:
        if utils.dico_placement[dp] not in poles:
            node_liste.remove(dp)


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

def callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon):
    elements, node_liste =   filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon)
    elements2 = utils.genere_sous_graphe(data['id'], node_liste, domaine)
    return elements2



@app.callback(
    Output('stored-tap-data', 'data'),
    Input('cytoscape', 'tapNodeData')
)
def update_store(tap_node_data):
    if tap_node_data:
        return tap_node_data  # Stocker les données du nœud cliqué
    return None  # Réinitialiser si aucune interaction





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
    Input('add-node-btn', 'n_clicks'),
    Input('cytoscape', 'layout'),
    Input('stored-tap-data', 'data'),
    Input('stored-elements', 'data'),
    Input('stored-data-table', 'data'),
    Input('zoom-flag', 'data')
    ],
    [State('node-nom', 'value'),
    State('node-niveau', 'value'),
    State('node-domaine', 'value'),
    State('node-nature', 'value'),
    State('node-influence', 'value'),
    State('node-interaction', 'value'),
    State('node-doublon', 'value'),
    State('node-acronyme', 'value'),
    State('cytoscape', 'elements')]
)


def update_cytoscape_table(tab,niveau, domaine_principal1,  domaine_principal2,  domaine_principal3, domaine1 , domaine2, domaine3, poles1, poles2, poles3, nature, doublon,
                        n_clicks, layout, stored_data,stored_elements,data_table,zoom_flag, nom, niveau_val, domaine_val, nature_val, influence_val, interaction_val, doublon_val, acronyme_val,
                        elements):
    

    domaine = domaine1 + domaine2 + domaine3
    domaine_principal = domaine_principal1 + domaine_principal2 + domaine_principal3
    poles = poles1 + poles2 + poles3

    table_data = data_table

    stored_data_clean = False
    edges_width = 0
    data = stored_elements

        

    if zoom_flag:
        elements = callback_sous_graphe(data, niveau, domaine_principal, domaine, poles, nature, doublon)
        edges_width = 1
    else:
        elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon)


    if stored_data and (not n_clicks and tab == "onglet2"):
        
        if stored_data['id'] in utils.domaine_principal_options :
            if not(zoom_flag):
                elements = callback_sous_graphe(stored_data, niveau, domaine_principal, domaine, poles, nature, doublon)
                edges_width = 1
                zoom_flag = True
            else:
                elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon)
                zoom_flag = False
                stored_data_clean = True

        # Mise à jour des données pour la table

            

            return elements, table_data, layout, stored_data_clean, utils.generate_stylesheet(utils.df_nodes, edges_width), stored_data, data_table, zoom_flag
        
        else:
            stored_data_clean = True
            elements, _ = filtres_callbacks(niveau, domaine_principal, domaine, poles, nature, doublon)
            node_id = stored_data['id']
            table_data = utils.df[utils.df['Nom'] == node_id].iloc[:, :11].to_dict('records')
            return elements, table_data, layout, stored_data_clean, utils.generate_stylesheet( utils.df_nodes, edges_width),  stored_elements, table_data, zoom_flag



    
    

    # Ajouter un nœud si le bouton est cliqué
    if n_clicks and not stored_data:
        # Créer un nouveau nœud
        new_node = {
            'data': {'id': nom, 'label': nom},
            'classes': 'node-class'
        }

        # Ajouter le nœud à la liste d'éléments
        elements.append(new_node)
        
        # Ajouter le nœud au dataframe (ceci est optionnel, selon votre logique)
        utils.df.loc[len(utils.df)] = [nom, niveau_val, domaine_val, nature_val, influence_val, interaction_val, doublon_val, acronyme_val]


    return elements, table_data, layout, True, utils.generate_stylesheet(utils.df_nodes, edges_width), stored_elements, data_table, zoom_flag

if __name__ == "__main__":
    app.run_server(debug=True, port = 8051)


