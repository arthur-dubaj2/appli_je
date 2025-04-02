from dash import html
import utils



legende = html.Div([
                        #html.H2('Légende'),
                        html.H3('Niveau'),
                        html.Div([
                            html.Div(style={'background-color': '#0074D9', 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.niveau_unique[0]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': '#0074D9', 'width': '20px', 'height': '20px', 'display': 'inline-block', 'clip-path': 'polygon(50% 0%, 0% 100%, 100% 100%)'}),
                            html.Span(f" : {utils.niveau_unique[2]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': '#0074D9', 'width': '20px', 'height': '20px', 'display': 'inline-block', 'clip-path': 'inset(0 0 0 0 round 0)'}),
                            html.Span(f" : {utils.niveau_unique[1]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': '#0074D9', 'width': '20px', 'height': '20px', 'display': 'inline-block', 'clip-path': 'polygon(50% 0%, 0% 50%, 50% 100%, 100% 50%)'}),
                            html.Span(f" : {utils.niveau_unique[3]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.H3('Nature'),
                        html.Div([
                            html.Div(style={'background-color': utils.couleur_dico[utils.nature_unique[0]], 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.nature_unique[0]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': utils.couleur_dico[utils.nature_unique[1]], 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.nature_unique[1]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': utils.couleur_dico[utils.nature_unique[2]], 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.nature_unique[2]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color':utils. couleur_dico[utils.nature_unique[3]], 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.nature_unique[3]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                        html.Div([
                            html.Div(style={'background-color': utils.couleur_dico[utils.nature_unique[4]], 'width': '20px', 'height': '20px', 
                                'border-radius': '50%', 'display': 'inline-block'}),
                            html.Span(f" : {utils.nature_unique[4]}", style={'margin-left': '10px'})
                        ], style={'margin-bottom': '10px'}),
                    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'})