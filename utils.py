import dash
import dash_cytoscape as cyto
from dash import dash_table
from dash import html
import networkx as nx
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import random
import dash_bootstrap_components as dbc
import dash_auth



#Fonciton permettant de générer une couleur aléatoire

def generate_random_color():
    r = 10 * random.randint(1, 25)
    b = 10 * random.randint(1,25)
    g = 10 * random.randint(1,25)
    return f'rgb({r}, {g}, {b})'



#Importation de la bdd

df = pd.read_excel('database2.xlsx')
df.columns = ['Nom','Acronyme', 'Niveau', 'Pole', 'Domaine_principal','Domaine',  'Nature', 'Influence', 'Interaction', 'Doublon', 'Commentaires', 'Site',1,2]
# Correction du FutureWarning : conversion explicite avant fillna
for col in df.columns:
    if df[col].dtype == 'float64' or df[col].dtype == 'int64':
        df[col] = df[col].astype('object')
df.fillna('nan', inplace=True)

df['Pole'] = df['Pole'].replace("Utiliser l'hydrogène", "Utiliser")
df['Pole'] = df['Pole'].replace("Déployer l'hydrogène", "Déployer")


taille_df = df.shape[0]

#IDENTIFICATION DES DOUBLONS A L'AIDE D'UN NUMÉRO

# Dictionnaire pour suivre les occurrences des valeurs
occurrences = {}

# Fonction pour ajouter un suffixe numérique aux doublons
def ajouter_suffixe(valeur):
    if valeur in occurrences:
        occurrences[valeur] += 1
        return f"{valeur}_{occurrences[valeur]}"
    else:
        occurrences[valeur] = 0
        return valeur

# Appliquer la fonction à la colonne 'Nom'
df['Nom'] = df['Nom'].apply(ajouter_suffixe)



nodes = []

entreprises = df['Nom'].tolist()


#On récupère tous les domaines principaux

domaine_principal_options= df['Domaine_principal'].unique()

#On ajoute les pôles
nodes.append("Déployer")
nodes.append("Utiliser")
nodes.append("Produire")



#On relie les domaines principaux à leurs pôles

dico_placement = {}
nbr_dom_p_pole = {'Déployer' : 0, 'Utiliser' : 0, 'Produire' : 0}

for d in domaine_principal_options:
    nodes.append(d) #On ajoute le noeud à la structure de données
    d_pole = df.loc[df['Domaine_principal'] == d, 'Pole'].iloc[0]
    dico_placement[d] = d_pole
    nbr_dom_p_pole[d_pole] += 1





edges = []
for node in nodes:
    if node in dico_placement.keys():
        edges.append((node, dico_placement[node]))


#Ajout des entreprises dans le sous-graphe de leur domaine

#On construit un dictionnaire comptant le nombre de noeuds dans chaque domaine
domaine_options = df['Domaine'].unique()
nbr_noeuds_per_dom = {}



for d in domaine_options:
    nbr_noeuds_per_dom[d] = 0

dico_angle_2 = nbr_noeuds_per_dom.copy()

for e in entreprises:
    nodes.append(e)
    e_dom_princ = df.loc[df['Nom'] == e, 'Domaine_principal'].iloc[0]
    e_dom = df.loc[df['Nom'] == e, 'Domaine'].iloc[0]
    nbr_noeuds_per_dom[e_dom] += 1
    edges.append((e, e_dom_princ))


G= nx.Graph()
G.add_edges_from(edges)

#PERSONNALISATION DE CHAQUE NOEUD EN FONCTION DE SES CARACTERISTIQUES

df_nodes = pd.DataFrame()
df_nodes['Shape'] = None
df_nodes['Couleur'] = None
df_nodes['Taille'] = None
df_nodes['Label'] = None
df_nodes['Label_Couleur'] = None
df_nodes['Label_Size'] = None
couleur_dico = dict()
forme_dico = dict()


niveau_unique  = df['Niveau'].unique()
nature_unique = df['Nature'].unique()

# Palette de couleurs officielle France Hydrogène
# Couleurs de la charte graphique FH
professional_colors = [
    '#03a3ff',     # Bleu FH principal
    '#88c000',     # Vert FH
    '#ff9e00',     # Orange FH
    '#003a91',     # Bleu foncé FH
    '#7db8e8',     # Bleu clair dérivé
    '#b3d84d',     # Vert clair dérivé
    '#ffbb66',     # Orange clair dérivé
    '#4d7ab8',     # Bleu moyen dérivé
]

for idx, d in enumerate(nature_unique):
    if idx < len(professional_colors):
        couleur_dico[d] = professional_colors[idx]
    else:
        rgb = generate_random_color()
        while (rgb in list(couleur_dico.values())):
            rgb = generate_random_color()
        couleur_dico[d] = rgb

forme_dico[niveau_unique[0]] = 'ellipse'
forme_dico[niveau_unique[1]] = 'rectangle'
forme_dico[niveau_unique[2]] = 'triangle'
forme_dico[niveau_unique[3]] = 'diamond'


#Création d'un dictionnaire stockant le nombre d'entreprises dans chaque domaine principal

dico_nbr_dom = {}

for d in domaine_principal_options:
    dico_nbr_dom[d] = 0

#Création d'un dictionnaire stockant les angles en évolution pour chaque ilôt

dico_coord_dom = dico_nbr_dom.copy()

dico_angles_entr = dico_nbr_dom.copy()

#Création d'un dictionnaire stockant les coordonnées de chaque domaine

dico_coord_poles = {'Produire' : (650,-400), 'Déployer' : (0, 500), 'Utiliser' : (-900,-400)}

#Création de la DF df_nodes stockant les paramètres graphiques de chaque noeud



for row in df.itertuples():
    dico_nbr_dom[row.Domaine_principal] += 1



    shape = forme_dico[row.Niveau]
    couleur = couleur_dico[row.Nature]
    taille = row.Influence * 8
    acronyme = df.loc[df['Nom'] == row.Nom, 'Acronyme'].iloc[0]

    if row.Doublon == "Doublon positif":
        l_color = 'rgb(0,255,0)'
    elif row.Doublon == "Doublon négatif":
        l_color = 'rgb(255,0,0)'
    else:
        l_color = 'rgb(0,0,0)'

    if row.Influence != 'nan':
        label_size = str(int(row.Influence) * 3 + 10)
    else:
        label_size = 15
    ligne = [ shape, couleur, taille, acronyme, l_color, label_size]
    df_nodes.loc[len(df_nodes)] = ligne


df_nodes.fillna({'Taille' : 30}, inplace=True)
df_nodes['id'] = list(df['Nom'])

poles = ['Produire', 'Utiliser', 'Déployer']

base_liste = list(domaine_principal_options) + poles



# Obtenir toutes les options uniques pour chaque checklist
niveau_options = df['Niveau'].unique()


nature_options = df['Nature'].unique()
influence_options = df['Influence'].unique()
interaction_options = df['Interaction'].unique()
doublon_options = df['Doublon'].unique()


#Couleur dans l'affichage des filtres - Charte France Hydrogène officielle

dicolor_poles = {
    'Produire' : '#03a3ff',     # Bleu FH principal
    'Utiliser' : '#88c000',     # Vert FH
    'Déployer' : '#ff9e00'      # Orange FH
}

dicolor_dp = {}
for dp in domaine_principal_options:
    dicolor_dp[dp] = dicolor_poles[dico_placement[dp]]

dicolor_domaine = {}

#dictionnaire reliant chaque domaine à son domaine principal
dico_sous_graphe = {}
for d in domaine_principal_options:
    dico_sous_graphe[d] = []



for d in domaine_options:
    style_ligne = ['ellipse','transparent', 150, d, 'rgb(0,0,0)', 20, d ]
    df_nodes.loc[len(df_nodes)] = style_ligne
    assoc_dp = df.loc[df['Domaine'] == d, 'Domaine_principal'].iloc[0]
    dicolor_domaine[d] = dicolor_dp[assoc_dp]
    dico_sous_graphe[assoc_dp].append(d)

#Ajout de noeuds "repères" pour chaque domaine

for p in poles:
     # Pôles : augmentation de la taille pour accommoder le texte, fond semi-transparent
     df_nodes.loc[len(df_nodes)] = ['rectangle', dicolor_poles[p], 200, p, 'white', 20, p ]


temp_dico = {'Produire' : 0, 'Utiliser' : 0, 'Déployer' : 0}

for dp in domaine_principal_options:
    # Domaines principaux : rectangles arrondis pour meilleure lisibilité
    df_nodes.loc[len(df_nodes)] = ['roundrectangle', 'white', 180, dp,  dicolor_dp[dp], 18, dp]
    index = temp_dico[dico_placement[dp]]
    temp_dico[dico_placement[dp]] += 1
    angle = index * 360 / nbr_dom_p_pole[dico_placement[dp]]
    x0,y0 = dico_coord_poles[dico_placement[dp]]
    x = x0 + np.cos(np.radians(angle)) * 500
    y = y0 + np.sin(np.radians(angle)) * 500
    dico_coord_dom[dp] = (x,y)


df_nodes.loc[len(df_nodes)] = ['ellipse',dicolor_poles['Produire'], 75, 'IM', 'rgb(0,0,0)', 15, 'Industrie Manufacturière']



dico_coord_dp2 = {
    'Décarbonation' : (-400.0, -400.0),
    'Energie' : (1550.0, -400.0),
    'Industrie' : (-900.0, 100.0),
    'Métaux' : (650.0000000000001, 33.012701892219354),
    'Transport' : (-1500.0, -399.99999999999994),
    'Construction' : (-900.0000000000001, -900.0),
    'Aménagement des territoires' : (500.0, 500.0),
    'Support' : (-500.0, 500.00000000000006),
    'Test' : (649.9999999999998, -833.0127018922192)

}

dicoeff = {
    'Décarbonation' : 1,
    'Energie' : 3.5,
    'Industrie' : 1,
    'Métaux' : 1,
    'Transport' : 1.9,
    'Construction' : 1,
    'Aménagement des territoires' : 1,
    'Support' : 1,
    'Test' : 1

}

#Fonction calculant la position de chaque noeud



def position(nom, dico_nbr):

    x,y = 0,0
    if nom in poles:
        x,y = dico_coord_poles[nom]
        
    elif nom in domaine_principal_options:
        x,y = dico_coord_dp2[nom]
        print(nom, x, y)
    else:
        dom_princ = df.loc[df['Nom'] == nom, 'Domaine_principal'].iloc[0]
        interaction = df.loc[df['Nom'] == nom, 'Interaction'].iloc[0]
        dico_angles_entr[dom_princ] += 1 
        angle = dico_angles_entr[dom_princ] * 360 / dico_nbr[dom_princ]
        rayon = 35 * (5 - interaction) * dicoeff[dom_princ]
        x0, y0 = dico_coord_dp2[dom_princ]
        x = x0 + np.cos(np.radians(angle)) * rayon
        y = y0 + np.sin(np.radians(angle)) * rayon


    return {'x' : x, 'y' : y}


#On construit un dictionnaire reliant chaque domaine principal à ses sous domaines

dico_pos2 = dico_sous_graphe.copy()


def position2(nom, domaineFiltres, dico_angles):
    dico_pos_domaines = {}
    nbr_domaine = len(domaineFiltres)
    i = 1

    if nom in domaine_principal_options:
        return {'x' : 0, 'y' : 0}
    
    if nbr_domaine == 0:
        return {'x' : 0, 'y' : 0}

    else:
        for d in domaineFiltres:
            dico_pos_domaines[d] = 35 + (i * (360 / nbr_domaine))
            i += 1
        dico_pos_domaines['Généraliste '] = 35 + (i * (360 / nbr_domaine))

        
        x0 = 0
        y0 = 0
        x = 0
        y = 0
        if nom in domaineFiltres or nom == 'Généraliste ':
            angle =  dico_pos_domaines[nom]
            x = np.cos(np.radians(angle)) * 500
            y = np.sin(np.radians(angle)) * 500
            
        else:
            interaction = df.loc[df['Nom'] == nom, 'Interaction'].iloc[0]
            domaine_assoc = df.loc[df['Nom'] == nom, 'Domaine'].iloc[0]
            x0 = np.cos(np.radians(dico_pos_domaines[domaine_assoc])) * 500
            y0 = np.sin(np.radians(dico_pos_domaines[domaine_assoc])) * 500
            dico_angle_2[domaine_assoc] += 1
            x = x0 + np.cos(np.radians(dico_angle_2[domaine_assoc] * (360/dico_angles[domaine_assoc]))) * (40 * (5 -interaction))
            y = y0 + np.sin(np.radians(dico_angle_2[domaine_assoc] * (360/dico_angles[domaine_assoc]))) * (40 * (5 -interaction))

        return {'x' : x, 'y' : y}


# Convertir le graphe en format compatible avec Dash Cytoscape
nodes = [{'data': {'id': node, 'label': node }, 'position' : position(node, dico_nbr_dom)} for node in G.nodes]
edges = [{'data': {'source': source, 'target': target}} for source, target in G.edges]


#Fonction créant le sous graphe après un click sur le domaine principal



def genere_sous_graphe(dom_princ, nl, domaine_liste):
    node_liste = list(set((df[df["Domaine_principal"] == dom_princ]['Nom']).tolist()) & set(nl))  #Méthode pour effectuer un ET logique entre les listes
    node_liste.append(dom_princ)
    node_liste.append('Généraliste ')
    new_edges = []
    #new_edges = [{'data': {'source': 'Généraliste ', 'target': dom_princ}}]
    domaine_filtres = list(set(dico_sous_graphe[dom_princ]) & set(domaine_liste))
    d_angles_npd = {}
    for dom in domaine_filtres:
        d_angles_npd[dom] = 0
    d_angles_npd['Généraliste '] = 0
    node_liste += domaine_filtres
    for source in node_liste:
        if source not in base_liste and source not in dico_sous_graphe[dom_princ] and source != 'Généraliste ':
            dom = df.loc[df['Nom'] == source, 'Domaine'].iloc[0]
            new_edges.append({'data': {'source': source, 'target': dom}})
            d_angles_npd[dom] += 1

    


    elements = [
        {
            'data': {'id': node, 'label': node}, 'position' : position2(node, domaine_filtres, d_angles_npd)
        }
        for node in node_liste
    ] + new_edges

    return elements


#Génération de la stylesheet CSS des noeuds avec style amélioré

def generate_stylesheet(df_nodes_param, edges_width):
    stylesheet = []

    bo = 0.9
    for _, row in df_nodes_param.iterrows():
        if row['Label'] in base_liste + ['IM', 'ADT'] + list(domaine_options):
            text_valign = 'center'
            bo = 0
            # Style spécial pour les nœuds structurels (pôles et domaines principaux)
            is_structural = True
        else:
            text_valign = 'bottom'
            is_structural = False

        selector = f'node[id="{row["id"]}"]'
        
        # Style de base pour tous les nœuds
        style = {
            'label': row['Label'],
            'background-color': row['Couleur'],
            'background-opacity': bo,
            'width': row['Taille'],
            'height': row['Taille'],
            'shape': row['Shape'],
            'text-valign': text_valign,
            'text-halign': 'center',
            'color': row['Label_Couleur'],
            'font-size': row['Label_Size'],
            'font-weight': '600',
            'text-outline-color': '#ffffff',
            'text-outline-width': 2,
            'text-outline-opacity': 0.8,
            'transition-property': 'background-color, border-color, border-width',
            'transition-duration': '0.3s'
        }
        
        # Amélioration visuelle pour les nœuds d'organisation
        if not is_structural:
            # Ajouter une bordure basée sur le statut de doublon
            # Vérifier dans le dataframe si le nœud a un statut de doublon
            node_doublon_status = None
            if row['id'] in df['Nom'].values:
                try:
                    node_doublon_status = df[df['Nom'] == row['id']]['Doublon'].iloc[0]
                except:
                    pass
            
            if node_doublon_status == 'Doublon positif':
                style['border-width'] = 4
                style['border-color'] = 'rgb(0, 255, 0)'
            elif node_doublon_status == 'Doublon négatif':
                style['border-width'] = 4
                style['border-color'] = 'rgb(255, 0, 0)'
            else:
                style['border-width'] = 2
                style['border-color'] = 'rgba(0, 0, 0, 0.3)'
            
            # Ombre portée pour plus de profondeur
            style['shadow-blur'] = 15
            style['shadow-color'] = 'rgba(0, 0, 0, 0.3)'
            style['shadow-offset-x'] = 3
            style['shadow-offset-y'] = 3
            style['shadow-opacity'] = 0.5
        else:
            # Style pour les nœuds structurels (pôles et domaines principaux)
            if row['Label'] in poles:  # Pôles - style proéminent
                style['border-width'] = 4
                style['border-color'] = row['Couleur']
                style['border-opacity'] = 1
                style['text-outline-width'] = 0
                style['background-opacity'] = 0.95
                style['font-weight'] = '700'
                style['text-transform'] = 'uppercase'
                style['letter-spacing'] = '2px'
                style['shadow-blur'] = 20
                style['shadow-color'] = row['Couleur']
                style['shadow-opacity'] = 0.4
            elif row['Label'] in domaine_principal_options:  # Domaines principaux
                style['border-width'] = 2
                style['border-color'] = row['Label_Couleur']
                style['border-opacity'] = 0.9
                style['text-outline-width'] = 0
                style['background-opacity'] = 0.9
                style['font-weight'] = '600'
                
        stylesheet.append({'selector': selector, 'style': style})
    
    # Style global pour les arêtes
    stylesheet.append({
        'selector': 'edge',
        'style': {
            'width': edges_width,
            'line-color': '#bdc3c7',
            'opacity': 0.6,
            'curve-style': 'bezier',
            'target-arrow-shape': 'none'
        }
    })
    
    # Style pour les nœuds au survol
    stylesheet.append({
        'selector': 'node:hover',
        'style': {
            'border-width': 5,
            'border-color': '#3498db',
            'border-opacity': 1,
            'shadow-blur': 25,
            'shadow-color': '#3498db',
            'shadow-opacity': 0.7
        }
    })
    
    # Style pour les nœuds sélectionnés
    stylesheet.append({
        'selector': 'node:selected',
        'style': {
            'border-width': 6,
            'border-color': '#e74c3c',
            'border-opacity': 1,
            'background-opacity': 1,
            'overlay-color': '#e74c3c',
            'overlay-padding': 8,
            'overlay-opacity': 0.3
        }
    })

    return stylesheet


#Séparation des domaines en 3 pour la séparation des checklists

domaine_principal_options_1 , domaine_principal_options_2, domaine_principal_options_3 = [], [], []

domaine_options_1, domaine_options_2, domaine_options_3 = [], [], []

for dp in domaine_principal_options:
    if dico_placement[dp] == 'Produire':
        domaine_principal_options_1.append(dp)

    if dico_placement[dp] == 'Utiliser':
        domaine_principal_options_2.append(dp) 

    if dico_placement[dp] == 'Déployer':
        domaine_principal_options_3.append(dp)

for dp in domaine_principal_options_1:
    domaine_options_1 = domaine_options_1 + dico_sous_graphe[dp]
for dp in domaine_principal_options_2:
    domaine_options_2 = domaine_options_2 + dico_sous_graphe[dp]
for dp in domaine_principal_options_3:
    domaine_options_3 = domaine_options_3 + dico_sous_graphe[dp]