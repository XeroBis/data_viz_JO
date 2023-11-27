from dash import html, callback, Input, Output
from dash import dcc
import time

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
                    html.Div(
                        children=[
                            "",
                            dcc.Loading(
                                type="circle",
                                id="",
                                children=[
                                    html.Div(html.Div(id="loading_output"))
                                ],
                            ),],
                        id="div_loading",
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
                dcc.Graph(figure=jo_instance.get_repartitition_homme_femme(years=[2012, 2016]), config={
                          'displayModeBar': False}),
                id="div_graph_repartition_homme_femme"
            ),
            html.Div(
                dcc.Graph(figure=jo_instance.get_fig_participants_homme_femme(years=[2012, 2016]), config={
                          'displayModeBar': False}),
                id="div_graph_participant_homme_femme"
            ),
            html.Div(
                dcc.Graph(figure=jo_instance.get_fig_world(years=[2012, 2016]),
                          config={'displayModeBar': False}),
                id="div_graph_world"
            ),
            html.Div(
                dcc.Graph(figure=jo_instance.get_fig_medals(years=[2012, 2016]),
                          config={'displayModeBar': False}),
                id="div_graph_medals"
            ),
            html.Div(
                dcc.Graph(figure=jo_instance.get_fig_top_3(years=[2012, 2016]),
                          config={'displayModeBar': False}),
                id="div_graph_top_3"
            ),
            html.Div(
                dcc.Graph(
                    figure=jo_instance.get_fig_participants(
                        years=[2012, 2016]),
                    config={'displayModeBar': False}),
                id="div_graph_participants"
            ),
            html.Div(
                dcc.Graph(
                    figure=jo_instance.get_fig_repartition_sports(
                        years=[2012, 2016]),
                    config={'displayModeBar': False}),
                id="div_graph_participants_sports"
            ),
            html.Div(
                dcc.Graph(
                    figure=jo_instance.get_fig_age_sports(
                        years=[2012, 2016]),
                    config={'displayModeBar': False}),
                id="div_graph_age_sports"
            ),

        ], id="section_graph"
    )
    return section


layout = html.Div([
    section_top(),
    section_principale(),
])


@callback(
    Output("div_graph_repartition_homme_femme", "children"),
    Output("div_graph_participant_homme_femme", "children"),
    Output("div_graph_medals", "children"),
    Output("div_graph_world", "children"),
    Output("div_graph_top_3", "children"),
    Output("div_graph_participants", "children"),
    Output("div_graph_participants_sports", "children"),
    Output("div_graph_age_sports", "children"),
    Output("dropdown_pays", "options"),
    Output("loading_output", "children"),
    Input("dropdown_continent", "value"),
    Input("dropdown_pays", "value"),
    Input("slider_year", "value")
)
def update_graphs(continent, pays, years):
    print("change graph, continent:", continent,
          ", pays :", pays, ", years : ", years)
    start_time = time.time()
    graph_repart_h_f = dcc.Graph(figure=jo_instance.get_repartitition_homme_femme(
        years=years, country=pays, continent=continent), config={'displayModeBar': False})
    print("func : graph repart--- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_particip_h_f = dcc.Graph(figure=jo_instance.get_fig_participants_homme_femme(
        years=years, country=pays, continent=continent), config={'displayModeBar': False})
    print("func : particip h f --- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    l_country = jo_instance.get_list_country(years, continent)
    print("func : list country--- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_medals = dcc.Graph(figure=jo_instance.get_fig_medals(
        years, pays, continent), config={'displayModeBar': False})
    print("func : graph medals --- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_world = dcc.Graph(
        figure=jo_instance.get_fig_world(years, pays, continent))
    print("func : graph world--- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_top3 = dcc.Graph(figure=jo_instance.get_fig_top_3(
        years, continent), config={'displayModeBar': False})
    print("func : graph top3--- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_participants = dcc.Graph(figure=jo_instance.get_fig_participants(
        years, continent), config={'displayModeBar': False})
    print("func : graph participant--- %s seconds ---" %
          (time.time() - start_time))
    start_time = time.time()

    graph_participant_sport = dcc.Graph(figure=jo_instance.get_fig_repartition_sports(
        years, pays, continent), config={'displayModeBar': False})
    print("func : graph particpant sports--- %s seconds ---" %
          (time.time() - start_time))
    print("continent:", continent)
    graph_age_sport = dcc.Graph(figure=jo_instance.get_fig_age_sports(
        years, pays, continent), config={'displayModeBar': False})

    print("loading fini")
    return graph_repart_h_f, graph_particip_h_f, graph_medals, graph_world, graph_top3, graph_participants, graph_participant_sport, graph_age_sport, l_country, []
