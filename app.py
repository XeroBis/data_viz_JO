from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import accueil

# Création de l'application
app = Dash(__name__, suppress_callback_exceptions=True, update_title=None, prevent_initial_callbacks=True)

# server pour l'utilisation de gunicorn sur render
server = app.server

app.title = "JO 1896-2016"
app.layout = dbc.Container(
    fluid=True, 
    children=
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

@callback(
    Output('page-content', 'children'),
    Output('url', 'pathname'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """
    Affichage de la page selon l'URL et changement de l'url pour qu'il soit toujours propre
    """
    return accueil.layout, "accueil"



# Lancement de l'application
if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:8050/accueil')
    app.run_server(debug=True, port=8050, use_reloader=False)
