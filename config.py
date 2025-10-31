# Configuration centralisée pour la cartographie
# Ce fichier permet d'ajuster facilement les paramètres visuels et de positionnement

# Configuration des pôles et leurs positions
POLES_CONFIG = {
    'Produire': {
        'position': (800, -500),
        'couleur': 'rgb(0, 161, 255)',
        'rayon_placement': 600
    },
    'Déployer': {
        'position': (0, 600),
        'couleur': 'rgb(133, 195, 0)',
        'rayon_placement': 600
    },
    'Utiliser': {
        'position': (-1000, -500),
        'couleur': 'rgb(139, 30, 134)',
        'rayon_placement': 600
    }
}

# Configuration des domaines principaux et leurs positions
DOMAINES_PRINCIPAUX_CONFIG = {
    'Décarbonation': {'position': (-500, -500), 'facteur_rayon': 1.0},
    'Energie': {'position': (1700, -500), 'facteur_rayon': 3.5},
    'Industrie': {'position': (-1000, 100), 'facteur_rayon': 1.0},
    'Métaux': {'position': (800, 50), 'facteur_rayon': 1.0},
    'Transport': {'position': (-1600, -500), 'facteur_rayon': 1.9},
    'Construction': {'position': (-1000, -1000), 'facteur_rayon': 1.0},
    'Aménagement des territoires': {'position': (600, 600), 'facteur_rayon': 1.0},
    'Support': {'position': (-600, 600), 'facteur_rayon': 1.0},
    'Test': {'position': (800, -900), 'facteur_rayon': 1.0}
}

# Configuration des paramètres visuels
VISUAL_CONFIG = {
    'espacement_minimal': 80,  # Espacement minimal entre les nœuds
    'facteur_rayon_base': 35,  # Rayon de base pour le placement des entreprises
    'facteur_taille_influence': 8,  # Multiplicateur de taille basé sur l'influence
    'facteur_taille_label': 3,  # Multiplicateur de taille de police basé sur l'influence
    'taille_label_min': 10,  # Taille minimale de police
    'taille_label_max': 25,  # Taille maximale de police
    'opacite_noeuds': 0.9,  # Opacité des nœuds d'entreprise
    'opacite_domaines': 0.0,  # Opacité des nœuds de domaine (transparents)
    'largeur_arêtes': 0.5,  # Largeur des arêtes
    'couleur_arêtes': 'rgba(100, 100, 100, 0.3)'  # Couleur des arêtes
}

# Configuration de la légende
LEGENDE_CONFIG = {
    'largeur': '18%',
    'position': 'right',
    'espacement_elements': '15px',
    'couleur_fond': '#f8f9fa',
    'couleur_bordure': '#dee2e6',
    'rayon_bordure': '8px',
    'ombre': '0 2px 8px rgba(0,0,0,0.1)'
}

# Configuration responsive
RESPONSIVE_CONFIG = {
    'breakpoints': {
        'desktop': 1200,
        'tablet': 768,
        'mobile': 480
    },
    'facteurs_echelle': {
        'desktop': 1.0,
        'tablet': 0.8,
        'mobile': 0.6
    }
}

# Configuration des animations
ANIMATION_CONFIG = {
    'duree_transition': 500,  # Durée en millisecondes
    'type_easing': 'ease-in-out',
    'activer_animations': True
}

