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
df.fillna('nan', inplace=True)

df['Pole'] = df['Pole'].replace("Utiliser l'hydrogène", "Utiliser")
df['Pole'] = df['Pole'].replace("Déployer l'hydrogène", "Déployer")

taille_df = df.shape[0]

#Identification des doublons à l'aide d'un numéro

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
    print(d)
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

for d in nature_unique:
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

dico_coord_poles = {'Produire' : (0,-700), 'Déployer' : (-1000, 700), 'Utiliser' : (1000, 700)}

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


#Couleur dans l'affichage des filtres

dicolor_poles = {
    'Utiliser' : 'rgb(139,30,134)',
    'Déployer' : 'rgb(133,195,0)',
    'Produire' : 'rgb(0,161,255)'
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
    style_ligne = ['ellipse','rgb(100,100,200)', 75, d, 'rgb(0,0,0)', 15, d ]
    df_nodes.loc[len(df_nodes)] = style_ligne
    assoc_dp = df.loc[df['Domaine'] == d, 'Domaine_principal'].iloc[0]
    dicolor_domaine[d] = dicolor_dp[assoc_dp]
    dico_sous_graphe[assoc_dp].append(d)

#Ajout de noeuds "repères" pour chaque domaine

for p in poles:
     df_nodes.loc[len(df_nodes)] = ['ellipse',dicolor_poles[p], 0, p, 'rgb(0,0,0)', 15, p ]


temp_dico = {'Produire' : 0, 'Utiliser' : 0, 'Déployer' : 0}

for dp in domaine_principal_options:
    df_nodes.loc[len(df_nodes)] = ['ellipse', dicolor_dp[dp], 75, dp,  'rgb(0,0,0)', 15,dp]
    index = temp_dico[dico_placement[dp]]
    temp_dico[dico_placement[dp]] += 1
    angle = index * 360 / nbr_dom_p_pole[dico_placement[dp]]
    x0,y0 = dico_coord_poles[dico_placement[dp]]
    x = x0 + np.cos(np.radians(angle)) * 500
    y = y0 + np.sin(np.radians(angle)) * 500
    dico_coord_dom[dp] = (x,y)


df_nodes.loc[len(df_nodes)] = ['ellipse',dicolor_poles['Produire'], 75, 'IM', 'rgb(0,0,0)', 15, 'Industrie Manufacturière']





#Fonction calculant la position de chaque noeud



def position(nom, dico_nbr):

    x,y = 0,0
    if nom in poles:
        x,y = dico_coord_poles[nom]
        
    elif nom in domaine_principal_options:
        x,y = dico_coord_dom[nom]
    else:
        dom_princ = df.loc[df['Nom'] == nom, 'Domaine_principal'].iloc[0]
        interaction = df.loc[df['Nom'] == nom, 'Interaction'].iloc[0]
        dico_angles_entr[dom_princ] += 1 
        angle = dico_angles_entr[dom_princ] * 360 / dico_nbr[dom_princ]
        rayon = 35 * (5 - interaction)
        x0, y0 = dico_coord_dom[dom_princ]
        x = x0 + np.cos(np.radians(angle)) * rayon
        y = y0 + np.sin(np.radians(angle)) * rayon

    print(f'Coordonnées de {nom} : {x},{y}')

    return {'x' : x, 'y' : y}


#On construit un dictionnaire reliant chaque domaine principal à ses sous domaines

dico_pos2 = dico_sous_graphe.copy()
"""for d in dico_sous_graphe.keys():
    print(type(dico_pos2))
    print(dico_sous_graphe)
    dico_pos2[dico_sous_graphe[d]] = d"""


def position2(nom, domaineFiltres, dico_angles):
    dico_pos_domaines = {}
    nbr_domaine = len(domaineFiltres)
    i = 1

    if nom in domaine_principal_options:
        return {'x' : 0, 'y' : 0}

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

#On commence par créer une variable nous permettant de switcher entre le mode preset et le mode cose dans l'affichage du graphe


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


#Génération de la stylesheet CSS des noeuds

def generate_stylesheet(df, edges_width):
    stylesheet = []
    for _, row in df.iterrows():
        if row['Label'] in base_liste + ['IM', 'ADT'] + list(domaine_options):
            text_valign = 'center'
        else:
            text_valign = 'bottom'

        selector = f'node[id="{row["id"]}"]'
        style = {
            'label': row['Label'],
            'background-color': row['Couleur'],
            'width': row['Taille'],
            'height': row['Taille'],
            'shape' : row['Shape'],
            'text-valign':text_valign,  # Alignement vertical au centre
            'text-halign': 'center',
            'color' : row['Label_Couleur'],
            'font-size' : row['Label_Size']
        }
        stylesheet.append({'selector': selector, 'style': style})
    
    stylesheet.append({
        'selector': 'edge',
        'style': {
            'width': edges_width,  # Taille des arêtes réduite à zéro (invisible)
            'line-color': 'transparent'  # Couleur transparente
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