from dash import html
import utils

# Couleurs officielles France Hydrogène
FH_BLUE = '#03a3ff'
FH_GREEN = '#88c000'
FH_ORANGE = '#ff9e00'
FH_DARK_BLUE = '#003a91'

# Styles professionnels pour la légende - Hauteur réduite
legend_container_style = {
    'backgroundColor': 'white',
    'borderRadius': '8px',
    'padding': '20px',
    'boxShadow': '0 2px 12px rgba(0, 0, 0, 0.08)',
    'border': f'1px solid {FH_BLUE}',
    'width': '280px',
    'maxHeight': '650px',
    'overflowY': 'auto'
}

section_style = {
    'marginBottom': '20px',
    'paddingBottom': '16px',
    'borderBottom': '1px solid #e0e0e0'
}

section_title_style = {
    'fontSize': '13px',
    'fontWeight': '700',
    'marginBottom': '12px',
    'color': FH_DARK_BLUE,
    'textTransform': 'uppercase',
    'letterSpacing': '0.5px',
    'borderLeft': f'4px solid {FH_BLUE}',
    'paddingLeft': '10px'
}

item_container_style = {
    'display': 'flex',
    'alignItems': 'center',
    'marginBottom': '10px',
    'padding': '6px',
    'borderRadius': '4px',
    'backgroundColor': '#fafafa'
}

item_label_style = {
    'fontSize': '12px',
    'color': '#424242',
    'fontWeight': '500',
    'marginLeft': '10px'
}

def create_shape_legend(shape_type, label):
    """Crée un élément de légende pour une forme"""
    shapes = {
        'circle': {'borderRadius': '50%'},
        'triangle': {'width': '0', 'height': '0', 'borderLeft': '10px solid transparent', 
                     'borderRight': '10px solid transparent', 'borderBottom': f'18px solid {FH_BLUE}',
                     'backgroundColor': 'transparent'},
        'rectangle': {'borderRadius': '2px'},
        'diamond': {'width': '14px', 'height': '14px', 'transform': 'rotate(45deg)'}
    }
    
    base_style = {
        'width': '18px',
        'height': '18px',
        'backgroundColor': FH_BLUE,
        'display': 'inline-block',
        'minWidth': '18px'
    }
    
    shape_style = {**base_style, **shapes.get(shape_type, {})}
    
    return html.Div([
        html.Div(style=shape_style),
        html.Span(label, style=item_label_style)
    ], style=item_container_style)

def create_color_legend(color, label):
    """Crée un élément de légende pour une couleur"""
    return html.Div([
        html.Div(style={
            'width': '18px',
            'height': '18px',
            'backgroundColor': color,
            'borderRadius': '3px',
            'minWidth': '18px',
            'border': '1px solid rgba(0,0,0,0.1)'
        }),
        html.Span(label, style=item_label_style)
    ], style=item_container_style)

def create_size_legend(size, label):
    """Crée un élément de légende pour la taille"""
    return html.Div([
        html.Div(style={
            'width': f'{size}px',
            'height': f'{size}px',
            'backgroundColor': FH_BLUE,
            'borderRadius': '50%',
            'minWidth': f'{size}px',
            'border': '1px solid rgba(0,0,0,0.1)'
        }),
        html.Span(label, style=item_label_style)
    ], style=item_container_style)

def create_border_legend(border_color, label):
    """Crée un élément de légende pour les bordures"""
    return html.Div([
        html.Div(style={
            'width': '18px',
            'height': '18px',
            'backgroundColor': 'white',
            'borderRadius': '50%',
            'border': f'3px solid {border_color}',
            'minWidth': '18px'
        }),
        html.Span(label, style=item_label_style)
    ], style=item_container_style)

# Construction de la légende
legende = html.Div([
    # En-tête
    html.Div([
        html.H3('Légende', style={
            'fontSize': '16px',
            'fontWeight': '700',
            'margin': '0 0 6px 0',
            'color': FH_DARK_BLUE,
            'textTransform': 'uppercase',
            'letterSpacing': '1px'
        }),
        html.Div(style={
            'width': '100%',
            'height': '3px',
            'background': f'linear-gradient(90deg, {FH_GREEN} 0%, {FH_BLUE} 50%, {FH_ORANGE} 100%)',
            'marginBottom': '20px'
        })
    ]),
    
    # Section Niveau
    html.Div([
        html.H4('Niveau géographique', style=section_title_style),
        create_shape_legend('circle', utils.niveau_unique[0] if len(utils.niveau_unique) > 0 else 'International'),
        create_shape_legend('triangle', utils.niveau_unique[2] if len(utils.niveau_unique) > 2 else 'Europe'),
        create_shape_legend('rectangle', utils.niveau_unique[1] if len(utils.niveau_unique) > 1 else 'France'),
        create_shape_legend('diamond', utils.niveau_unique[3] if len(utils.niveau_unique) > 3 else 'Local'),
    ], style=section_style),
    
    # Section Nature
    html.Div([
        html.H4('Nature d\'organisation', style=section_title_style),
        html.Div([
            create_color_legend(utils.couleur_dico[nature], nature)
            for nature in utils.nature_unique
        ])
    ], style=section_style),
    
    # Section Influence
    html.Div([
        html.H4('Niveau d\'influence', style=section_title_style),
        create_size_legend(10, 'Faible (1)'),
        create_size_legend(16, 'Moyenne (2)'),
        create_size_legend(22, 'Élevée (3)'),
        create_size_legend(28, 'Très élevée (4)'),
        html.P('Taille du nœud = influence', 
               style={'fontSize': '10px', 'color': '#757575', 'marginTop': '8px', 'lineHeight': '1.3', 'fontStyle': 'italic'})
    ], style=section_style),
    
    # Section Doublons
    html.Div([
        html.H4('Statut de doublon', style=section_title_style),
        create_border_legend('rgb(46, 125, 50)', 'Doublon positif'),
        create_border_legend('rgb(198, 40, 40)', 'Doublon négatif'),
        create_border_legend('rgb(117, 117, 117)', 'Pas de doublon'),
    ], style=section_style),
    
    # Section Pôles
    html.Div([
        html.H4('Pôles principaux', style=section_title_style),
        create_color_legend(FH_BLUE, 'Produire'),
        create_color_legend(FH_GREEN, 'Utiliser'),
        create_color_legend(FH_ORANGE, 'Déployer'),
    ], style=section_style),
    
    # Instructions d'utilisation
    html.Div([
        html.H4('Navigation', style=section_title_style),
        html.Div([
            html.Div([
                html.Span('• ', style={'fontWeight': '700', 'color': FH_BLUE, 'fontSize': '14px'}),
                html.Span('Survolez pour infos', 
                         style={'fontSize': '11px', 'color': '#424242'})
            ], style={'marginBottom': '6px'}),
            html.Div([
                html.Span('• ', style={'fontWeight': '700', 'color': FH_BLUE, 'fontSize': '14px'}),
                html.Span('Clic sur domaine = zoom', 
                         style={'fontSize': '11px', 'color': '#424242'})
            ], style={'marginBottom': '6px'}),
            html.Div([
                html.Span('• ', style={'fontWeight': '700', 'color': FH_BLUE, 'fontSize': '14px'}),
                html.Span('Re-clic = vue globale', 
                         style={'fontSize': '11px', 'color': '#424242'})
            ])
        ], style={'paddingLeft': '6px'})
    ], style={'marginTop': '16px', 'paddingTop': '16px', 'borderTop': f'2px solid {FH_BLUE}'})
    
], style=legend_container_style)
