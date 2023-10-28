from dash import html, callback, Input, Output
from dash import dcc

from utils.graph import JO
jo_instance = JO()

# ------------------- LAYOUT ------------------- #


def section_top():
    section = html.Section(
        children=[
            html.Div(
                html.Div("Statistiques sur les JO 1896-2016", id="titre"),
                id="div_titre"
            ),
            html.Div(
                children=[
                    dcc.RangeSlider(1896, 2016, 4, value=[2012, 2016], marks={
                                    1896+i: str(1896+i) for i in range(0, 124, 4)}, id="slider_year"),
                    html.Div(
                        children=[
                            dcc.Dropdown(options=["ASIE", "EUROPE", "AFRIQUE", "OCÉANIE", "AMÉRIQUE"],
                                         id="dropdown_continent", placeholder='Sélection continent')
                        ],
                        id="div_dropdown_continent"
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(jo_instance.get_list_country(
                            ), id="dropdown_pays", placeholder='Sélection pays')
                        ],
                        id="div_dropdown_pays"
                    ),
                ],
                id="section_parametrage"
            ),
        ]

    )
    return section


def section_principale():

    section = html.Section(
        children=[
            html.Div(
                dcc.Graph(figure=jo_instance.get_repartitition_homme_femme(), config={
                          'displayModeBar': False}),
                id="div_graph_repartition_homme_femme"
            ),
            html.Div(
                dcc.Graph(figure=jo_instance.get_fig_medals(),
                          config={'displayModeBar': False}),
                id="div_graph_medals"
            )
        ], id="section_graph"
    )
    return section


layout = html.Div([
    section_top(),
    section_principale(),
])


@callback(
    Output("div_graph_repartition_homme_femme", "children"),
    Output("div_graph_medals", "children"),
    Output("dropdown_pays", "options"),
    Input("dropdown_continent", "value"),
    Input("dropdown_pays", "value"),
    Input("slider_year", "value")
)
def update_graphs(continent, pays, years):
    print("change graph, continent:", continent,
          ", pays :", pays, ", years : ", years)
    

    graph_repart_h_f = dcc.Graph(figure=jo_instance.get_repartitition_homme_femme(years=years, country=pays, continent=continent), config={'displayModeBar': False})
    l_country = jo_instance.get_list_country(years, continent)
    graph_medals = dcc.Graph(figure=jo_instance.get_fig_medals(years, pays, continent), config={'displayModeBar': False})
    return graph_repart_h_f, graph_medals, l_country
