import dash_cytoscape as cyto
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import utils

# Styles modernes pour les filtres
main_filter_container = {
    'background': 'linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%)',
    'minHeight': '100vh',
    'padding': '30px',
    'fontFamily': "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
}

filter_card_style = {
    'backgroundColor': 'white',
    'borderRadius': '15px',
    'padding': '25px',
    'marginBottom': '20px',
    'boxShadow': '0 8px 30px rgba(0, 0, 0, 0.08)',
    'border': '1px solid rgba(0, 0, 0, 0.05)',
    'transition': 'transform 0.2s ease, box-shadow 0.2s ease'
}

section_title_style = {
    'fontWeight': '700',
    'fontSize': '16px',
    'marginBottom': '16px',
    'color': '#003a91',
    'borderLeft': '4px solid #03a3ff',
    'paddingLeft': '12px',
    'letterSpacing': '0.5px',
    'textTransform': 'uppercase'
}

pole_container_style = {
    'backgroundColor': '#f8f9fa',
    'borderRadius': '12px',
    'padding': '20px',
    'marginBottom': '15px',
    'border': '2px solid transparent',
    'transition': 'all 0.3s ease'
}

checklist_label_style = {
    'display': 'block',
    'margin': '8px 0',
    'padding': '10px 15px',
    'borderRadius': '8px',
    'transition': 'all 0.2s ease',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '500'
}

checklist_label_style_inline = {
    'display': 'inline-block',
    'margin': '5px',
    'padding': '8px 12px',
    'borderRadius': '8px',
    'transition': 'all 0.2s ease',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '500'
}

filtres_tab = dcc.Tab(
    label='Filtres',
    value='onglet1',
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
            # En-tête
            html.Div([
                html.H1('Filtres de visualisation', style={
                    'color': '#003a91',
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'margin': '0 0 10px 0',
                    'letterSpacing': '0.5px'
                }),
                html.P('Sélectionnez les critères pour personnaliser la vue', style={
                    'color': '#666',
                    'fontSize': '14px',
                    'margin': '0 0 30px 0',
                    'fontWeight': '400'
                })
            ], style={'textAlign': 'center', 'marginBottom': '30px'}),

            # Grille des filtres
            html.Div([
                # Colonne gauche : Niveau, Nature, Doublon
                html.Div([
                    # Section Niveau
                    html.Div([
                        html.H4("Niveau", style=section_title_style),
                        dcc.Checklist(
                            id='checklist-Niveau',
                            options=[{'label': i, 'value': i} for i in utils.niveau_options],
                            value=utils.niveau_options,
                            labelStyle=checklist_label_style
                        ),
                    ], style=filter_card_style),

                    # Section Nature
                    html.Div([
                        html.H4("Nature", style=section_title_style),
                        dcc.Checklist(
                            id='checklist-Nature',
                            options=[{
                                'label': html.Div([
                                    html.Div(style={
                                        'width': '12px',
                                        'height': '12px',
                                        'borderRadius': '50%',
                                        'backgroundColor': utils.couleur_dico[i],
                                        'display': 'inline-block',
                                        'marginRight': '10px',
                                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.2)'
                                    }),
                                    html.Span(i, style={'verticalAlign': 'middle'})
                                ], style={'display': 'flex', 'alignItems': 'center'}),
                                'value': i
                            } for i in utils.nature_options],
                            value=utils.nature_options,
                            labelStyle=checklist_label_style
                        ),
                    ], style=filter_card_style),

                    # Section Doublon
                    html.Div([
                        html.H4("Doublon", style=section_title_style),
                        dcc.Checklist(
                            id='checklist-Doublon',
                            options=[{'label': i, 'value': i} for i in utils.doublon_options],
                            value=utils.doublon_options,
                            labelStyle=checklist_label_style
                        ),
                    ], style=filter_card_style),
                ], style={'flex': '1', 'marginRight': '20px'}),

                # Colonne droite : Pôles et domaines
                html.Div([
                    html.Div([
                        html.H4("Pôles et Domaines", style=section_title_style),
                        
                        # Pôle Produire
                        html.Div([
                            html.Div([
                                dcc.Checklist(
                                    id='checklist-Pole1',
                                    options=[{
                                        'label': html.Span([
                                            html.Div(style={
                                                'width': '14px',
                                                'height': '14px',
                                                'borderRadius': '50%',
                                                'backgroundColor': utils.dicolor_poles['Produire'],
                                                'display': 'inline-block',
                                                'marginRight': '10px',
                                                'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.2)'
                                            }),
                                            html.Span('PRODUIRE', style={
                                                'fontWeight': '700',
                                                'fontSize': '16px',
                                                'color': utils.dicolor_poles['Produire'],
                                                'letterSpacing': '0.5px'
                                            })
                                        ], style={'display': 'flex', 'alignItems': 'center'}),
                                        'value': 'Produire'
                                    }],
                                    value=['Produire'],
                                    labelStyle={'fontWeight': 'bold'}
                                ),
                                # Domaines principaux
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine_principal_1',
                                        options=[{
                                            'label': html.Div([
                                                html.Div(style={
                                                    'width': '8px',
                                                    'height': '8px',
                                                    'borderRadius': '50%',
                                                    'backgroundColor': utils.dicolor_dp[i],
                                                    'display': 'inline-block',
                                                    'marginRight': '8px'
                                                }),
                                                html.Span(i)
                                            ], style={'display': 'flex', 'alignItems': 'center'}),
                                            'value': i
                                        } for i in utils.domaine_principal_options_1],
                                        value=utils.domaine_principal_options_1,
                                        labelStyle={'marginLeft': '25px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '10px'}),
                                # Domaines
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine1',
                                        options=[{
                                            'label': html.Span(i, style={'fontSize': '13px'}),
                                            'value': i
                                        } for i in utils.domaine_options_1],
                                        value=utils.domaine_options_1,
                                        labelStyle={'marginLeft': '45px', 'fontSize': '13px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '5px'}),
                            ], style={'marginBottom': '25px'})
                        ], style={
                            **pole_container_style,
                            'borderColor': utils.dicolor_poles['Produire']
                        }),

                        # Pôle Utiliser
                        html.Div([
                            html.Div([
                                dcc.Checklist(
                                    id='checklist-Pole2',
                                    options=[{
                                        'label': html.Span([
                                            html.Div(style={
                                                'width': '14px',
                                                'height': '14px',
                                                'borderRadius': '50%',
                                                'backgroundColor': utils.dicolor_poles['Utiliser'],
                                                'display': 'inline-block',
                                                'marginRight': '10px',
                                                'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.2)'
                                            }),
                                            html.Span('UTILISER', style={
                                                'fontWeight': '700',
                                                'fontSize': '16px',
                                                'color': utils.dicolor_poles['Utiliser'],
                                                'letterSpacing': '0.5px'
                                            })
                                        ], style={'display': 'flex', 'alignItems': 'center'}),
                                        'value': 'Utiliser'
                                    }],
                                    value=['Utiliser'],
                                    labelStyle={'fontWeight': 'bold'}
                                ),
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine_principal_2',
                                        options=[{
                                            'label': html.Div([
                                                html.Div(style={
                                                    'width': '8px',
                                                    'height': '8px',
                                                    'borderRadius': '50%',
                                                    'backgroundColor': utils.dicolor_dp[i],
                                                    'display': 'inline-block',
                                                    'marginRight': '8px'
                                                }),
                                                html.Span(i)
                                            ], style={'display': 'flex', 'alignItems': 'center'}),
                                            'value': i
                                        } for i in utils.domaine_principal_options_2],
                                        value=utils.domaine_principal_options_2,
                                        labelStyle={'marginLeft': '25px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '10px'}),
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine2',
                                        options=[{
                                            'label': html.Span(i, style={'fontSize': '13px'}),
                                            'value': i
                                        } for i in utils.domaine_options_2],
                                        value=utils.domaine_options_2,
                                        labelStyle={'marginLeft': '45px', 'fontSize': '13px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '5px'}),
                            ], style={'marginBottom': '25px'})
                        ], style={
                            **pole_container_style,
                            'borderColor': utils.dicolor_poles['Utiliser']
                        }),

                        # Pôle Déployer
                        html.Div([
                            html.Div([
                                dcc.Checklist(
                                    id='checklist-Pole3',
                                    options=[{
                                        'label': html.Span([
                                            html.Div(style={
                                                'width': '14px',
                                                'height': '14px',
                                                'borderRadius': '50%',
                                                'backgroundColor': utils.dicolor_poles['Déployer'],
                                                'display': 'inline-block',
                                                'marginRight': '10px',
                                                'boxShadow': '0 2px 6px rgba(0, 0, 0, 0.2)'
                                            }),
                                            html.Span('DÉPLOYER', style={
                                                'fontWeight': '700',
                                                'fontSize': '16px',
                                                'color': utils.dicolor_poles['Déployer'],
                                                'letterSpacing': '0.5px'
                                            })
                                        ], style={'display': 'flex', 'alignItems': 'center'}),
                                        'value': 'Déployer'
                                    }],
                                    value=['Déployer'],
                                    labelStyle={'fontWeight': 'bold'}
                                ),
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine_principal_3',
                                        options=[{
                                            'label': html.Div([
                                                html.Div(style={
                                                    'width': '8px',
                                                    'height': '8px',
                                                    'borderRadius': '50%',
                                                    'backgroundColor': utils.dicolor_dp[i],
                                                    'display': 'inline-block',
                                                    'marginRight': '8px'
                                                }),
                                                html.Span(i)
                                            ], style={'display': 'flex', 'alignItems': 'center'}),
                                            'value': i
                                        } for i in utils.domaine_principal_options_3],
                                        value=utils.domaine_principal_options_3,
                                        labelStyle={'marginLeft': '25px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '10px'}),
                                html.Div([
                                    dcc.Checklist(
                                        id='checklist-Domaine3',
                                        options=[{
                                            'label': html.Span(i, style={'fontSize': '13px'}),
                                            'value': i
                                        } for i in utils.domaine_options_3],
                                        value=utils.domaine_options_3,
                                        labelStyle={'marginLeft': '45px', 'fontSize': '13px', **checklist_label_style_inline}
                                    ),
                                ], style={'marginTop': '5px'}),
                            ])
                        ], style={
                            **pole_container_style,
                            'borderColor': utils.dicolor_poles['Déployer']
                        })
                    ], style=filter_card_style)
                ], style={'flex': '2'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'gap': '20px'
            })
        ], style=main_filter_container)
    ]
)
