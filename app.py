import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import subprocess
import sys
import time
import os


# Liste des utilisateurs autorisés
VALID_USERNAME_PASSWORD_PAIRS = {
    "user1": "password1",
    "user2": "password2"
}

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout de la page de connexion
app.layout = html.Div(id="page-content", children=[
    html.Div([
        html.H2("Connexion", style={"textAlign": "center", "marginBottom": "20px"}),
        dbc.Input(id="username", placeholder="Nom d'utilisateur", type="text", className="mb-2"),
        dbc.Input(id="password", placeholder="Mot de passe", type="password", className="mb-2"),
        dbc.Button("Se connecter", id="login-button", color="primary", className="mt-2"),
        html.Div(id="login-message", style={"color": "red", "marginTop": "10px"}),

        # Ajout de l'image ici
        html.Img(
            src="assets/logo_FH.png", 
            style={
                "marginTop": "20px",
                "width": "60%",  # Ajuste la largeur (par exemple, "300px" pour une largeur fixe)
                "height": "auto",  # Garde le ratio de l'image
                "borderRadius": "8px"  # Ajoute des bords arrondis si nécessaire
            }
        )
    ], style={
        "width": "300px",
        "margin": "auto",
        "padding": "50px",
        "border": "1px solid #ccc",
        "borderRadius": "8px",
        "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)",
        "textAlign": "center"
    })
])


# Fonction pour lancer main.py en tant que sous-processus
def launch_main():
    print("Lancement de main.py...")
    subprocess.Popen(['python', 'main.py'])  # Lancer main.py comme un subprocess


# Callback pour vérifier les identifiants et rediriger vers la page principale
@app.callback(
    [Output("page-content", "children"),
     Output("login-message", "children")],
    [Input("login-button", "n_clicks")],
    [State("username", "value"), State("password", "value")]
)
def login(n_clicks, username, password):
    if n_clicks:
        if username in VALID_USERNAME_PASSWORD_PAIRS and VALID_USERNAME_PASSWORD_PAIRS[username] == password:
            # Lancer main.py en sous-processus
            launch_main()

        # Attendre un peu pour que Dash démarre
            time.sleep(2)

            print("test")
            return html.Div([
                html.H3("Connexion réussie !"),
                html.A("Cliquez ici pour accéder à la page principale", href="http://127.0.0.1:8051", target="_blank")
            ]), ""
            
        else:
            # Identifiants incorrects
            return dash.no_update, "Identifiant ou mot de passe incorrect."
    return dash.no_update, ""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)

