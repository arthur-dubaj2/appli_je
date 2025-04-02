@echo off

@echo off

REM Vérifier si Python est déjà installé
python --version >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Installation de Python...
    REM Lancez l'installateur Python (assurez-vous que le fichier python-installer.exe est dans le même répertoire)
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
) ELSE (
    echo Python est déjà installé.
)

REM Installer les dépendances nécessaires
echo Installation des bibliothèques requises...
pip install dash pandas dash-bootstrap-components dash-cytoscape networkx openpyxl

REM Lancer l'application
echo Lancement de l'application...
start cmd /k python "C:\Users\Arthur\Documents\ensimag\etudeje\projet_dang\app\pages\app.py"
start cmd /k python "C:\Users\Arthur\Documents\ensimag\etudeje\projet_dang\app\pages\main.py"







