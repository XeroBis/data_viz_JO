import pandas as pd
import plotly.graph_objs as go
import yaml
from collections import Counter


class JO:

    def __init__(self):
        self.data = pd.read_csv("data/athlete_events.csv")
        self.regions = pd.read_csv("data/noc_regions.csv")
        self.config = self.get_config()
        self.noc_unkown = []
        pass

    @staticmethod
    def get_config() -> dict:
        with open("config/config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config

    def get_number_of_(self, sex, year=None, country=None, continent=None):
        df_men = self.data[self.data["Sex"] == sex]
        if year is not None:
            df_men = df_men[df_men["Year"] == year]

        if country is not None and continent is None:
            df_men = df_men[df_men["NOC"] == self.get_noc_of_country(country)]
        elif continent is not None:
            df_men_sub = df_men.copy()
            for noc in self.config[continent]:
                df_men = pd.concat(
                    [df_men, df_men_sub[df_men_sub["NOC"] == noc]])
        return len(df_men)

    def get_list_country(self, years=None, continent=None):

        list_noc = []
        if years is not None:
            for year in years:
                data_2 = self.data[self.data["Year"] == year]
                list_noc.extend(data_2["NOC"].unique())
        else:
            list_noc.extend(self.data["NOC"].unique())
        list_country = []
        for noc in list_noc:
            region = self.regions.loc[self.regions["NOC"] == noc, "region"]
            if continent is not None:
                if noc in self.config[continent]:
                    if isinstance(region.iloc[0], str):
                        if region.iloc[0] not in list_country:
                            list_country.append(region.iloc[0])
            else:
                if isinstance(region.iloc[0], str):
                    if region.iloc[0] not in list_country:
                        list_country.append(region.iloc[0])

        return sorted(list_country)

    def get_country_of_noc(self, noc):
        noc = self.regions.loc[self.regions["NOC"] == noc, "region"]
        return noc.iloc[0]

    def get_noc_of_country(self, country):
        noc = self.regions.loc[self.regions["region"] == country, "NOC"]
        return noc.iloc[0]

    def get_noc_of_list_country(self, countries):
        noc = []
        for country in countries:
            noc.append(self.get_noc_of_country(country))
        return noc

    def get_region_of_noc(self, noc):

        pass

    def get_region_of_list_noc(self, nocs):
        regions = []
        for noc in nocs:
            regions.append(
                self.regions.loc[self.regions['NOC'] == noc, 'region'].item())
        return regions

    def get_liste_region(self, years=None, pays=None, continent=None):
        if pays is None:
            l_country = self.get_list_country(years, continent)

        else:
            l_country = [pays]
        l_noc = self.get_noc_of_list_country(l_country)
        l_region = self.get_region_of_list_noc(l_noc)
        return l_region

    def get_number_participant(self, years=None, noc=None):
        data = self.data
        particpant = 0
        if noc is not None:
            data = data[data["NOC"] == noc]
        if years is not None:
            for year in years:
                data_temp = data[data["Year"] == year]
                particpant += len(data_temp["Name"].unique())
        else:
            return len(data["Name"].unique())

        return particpant

    #################
    ##### GRAPH #####
    #################

    # Répartition H-F #
    def get_repartitition_homme_femme(self, years=None, country=None, continent=None):
        nb_man = 0
        nb_woman = 0
        if years is not None:
            if years[0] == years[1]:
                tab_years = [years[0]]
            else:
                tab_years = range(years[0], years[1]+4, 4)
        else:
            tab_years = range(1896, 2020, 4)
        for year in tab_years:
            nb_man += self.get_number_of_("M", year, country, continent)
            nb_woman += self.get_number_of_("F", year, country, continent)

        bars = []
        bars.append(go.Bar(name="% of men", x=["Homme"], y=[
                    100*nb_man/(max(nb_man+nb_woman, 1))]))
        bars.append(go.Bar(name="% of women", x=["Femme"], y=[
                    100*nb_woman/(max(nb_man+nb_woman, 1))]))
        labels = ["Homme", "Femmes"]
        values = [100*nb_man/(max(nb_man+nb_woman, 1)),
                  100*nb_woman/(max(nb_man+nb_woman, 1))]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(
            title="Répartition Homme Femme",
        )
        return fig

    def get_fig_participants_homme_femme(self, years=None, country=None, continent=None):
        nb_man = 0
        nb_woman = 0
        if years is not None:
            if years[0] == years[1]:
                tab_years = [years[0]]
            else:
                tab_years = range(years[0], years[1]+4, 4)
        else:
            tab_years = range(1896, 2020, 4)
        for year in tab_years:
            nb_man += self.get_number_of_("M", year, country, continent)
            nb_woman += self.get_number_of_("F", year, country, continent)

        bars = []
        bars.append(go.Bar(name="Nombre d'homme", x=["Homme"], y=[nb_man]))
        bars.append(go.Bar(name="NUmber de femme", x=["Femme"], y=[nb_woman]))

        fig = go.Figure(data=bars)

        fig.update_layout(
            barmode='stack',
            xaxis_title="Nombre de participant Homme Femme", yaxis_title="",
            title="",
            showlegend=False
        )
        return fig

    def get_medals(self, years=None, noc=None):

        if years is not None:
            if years[0] == years[1]:
                tab_years = [years[0]]
            else:
                tab_years = range(years[0], years[1]+4, 4)
        else:
            tab_years = range(1896, 2020, 4)

        df_medal = pd.DataFrame()
        for year in tab_years:
            df_medal = pd.concat(
                [self.data[self.data["Year"] == year], df_medal])
        if noc is not None:
            df_medal = df_medal[df_medal["NOC"] == noc]
        res = {"Or": 0, "Argent": 0, "Bronze": 0}
        # df_medal.to_csv("data/test_france.csv")
        df_medal = df_medal.groupby(
            ["Event", "Medal"], as_index=False).agg("count")

        res["Or"] = len(df_medal[df_medal["Medal"] == "Gold"])
        res["Argent"] = len(df_medal[df_medal["Medal"] == "Silver"])
        res["Bronze"] = len(df_medal[df_medal["Medal"] == "Bronze"])
        return res

    def get_fig_medals(self, years=None, country=None, continent=None):
        medals = Counter({"Or": 0, "Argent": 0, "Bronze": 0})
        if country is not None:
            medals = Counter(self.get_medals(
                years, self.get_noc_of_country(country)))
        elif continent is not None:
            for noc in self.config[continent]:
                medals += Counter(self.get_medals(years, noc))
        else:
            medals = Counter(self.get_medals(years))
        fig = go.Figure(
            data=go.Bar(
                x=["Or", "Argent", "Bronze"],
                y=[medals["Or"], medals["Argent"], medals["Bronze"]],
                marker=dict(color=["#FFD700", "#C0C0C0", "#614e1a"])
            )
        )

        fig.update_layout(
            barmode='stack',
            xaxis_title="Nombre de médailles",
            title="",
            showlegend=False
        )
        return fig

    def get_fig_world(self, years=None, pays=None, continent=None):
        list_region = self.get_liste_region(years, pays, continent)
        fig = go.Figure(go.Scattergeo())
        fig.update_geos(projection_type="natural earth", showcountries=True)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.add_traces(
            go.Choropleth(
                locations=list_region,
                locationmode="country names",
                z=[i for i in range(1, len(list_region)+1)],
                colorbar=None,
                showscale=False
            )
        )
        return fig

    def get_fig_top_3(self, years=None, continent=None):
        res = {
            "1": {"country": "", "Or": 0, "Argent": 0, "Bronze": 0},
            "2": {"country": "", "Or": 0, "Argent": 0, "Bronze": 0},
            "3": {"country": "", "Or": 0, "Argent": 0, "Bronze": 0}
        }
        l_country = self.get_list_country(years, continent)
        l_nocs = self.get_noc_of_list_country(l_country)
        for noc in l_nocs:
            id_to_change = 0
            check_argent = False
            check_bronze = False
            medals = self.get_medals(years, noc)
            if medals["Or"] >= res["1"]["Or"]:
                id_to_change = 1
                check_argent = medals["Or"] == res["1"]["Or"]
            elif medals["Or"] >= res["2"]["Or"]:
                id_to_change = 2
                check_argent = medals["Or"] == res["2"]["Or"]

            elif medals["Or"] >= res["3"]["Or"]:
                id_to_change = 3
                check_argent = medals["Or"] == res["3"]["Or"]

            if check_argent:
                if medals["Argent"] >= res[str(id_to_change)]["Argent"]:
                    check_bronze = medals["Argent"] == res[str(
                        id_to_change)]["Argent"]

            if check_bronze:
                if medals["Bronze"] < res[str(id_to_change)]["Bronze"]:
                    id_to_change = id_to_change+1

            if id_to_change == 1:
                res["3"] = res["2"]
                res["2"] = res["1"]
                res["1"] = {
                    "country": self.get_country_of_noc(noc),
                    "Or": medals["Or"],
                    "Argent": medals["Argent"],
                    "Bronze": medals["Bronze"]
                }

            if id_to_change == 2:
                res["3"] = res["2"]
                res["2"] = {
                    "country": self.get_country_of_noc(noc),
                    "Or": medals["Or"],
                    "Argent": medals["Argent"],
                    "Bronze": medals["Bronze"]
                }

            if id_to_change == 3:
                res["3"] = {
                    "country": self.get_country_of_noc(noc),
                    "Or": medals["Or"],
                    "Argent": medals["Argent"],
                    "Bronze": medals["Bronze"]
                }

        bars = []
        # marker=dict(color=["#", "#C0C0C0", "#614e1a"])
        colors = {
            'Or': '#FFD700',
            'Argent': '#C0C0C0',
            'Bronze': '#614e1a'}
        bars.append(
            go.Bar(
                name="Or",
                x=[res["1"]["country"], res["2"]["country"], res["3"]["country"]],
                y=[res["1"]["Or"], res["3"]["Or"], res["3"]["Or"]],
                marker_color=colors["Or"]
            )
        )
        bars.append(
            go.Bar(
                name="Argent",
                x=[res["1"]["country"], res["2"]["country"], res["3"]["country"]],
                y=[res["1"]["Argent"], res["2"]["Argent"], res["3"]["Argent"]],
                marker_color=colors["Argent"]
            )
        )
        bars.append(
            go.Bar(
                name="Bronze",
                x=[res["1"]["country"], res["2"]["country"], res["3"]["country"]],
                y=[res["1"]["Bronze"], res["2"]["Bronze"], res["3"]["Bronze"]],
                marker_color=colors["Bronze"]
            )
        )
        fig = go.Figure(data=bars)

        fig.update_layout(
            barmode='group',
            xaxis_title="TOP 3 nombres de médailles", yaxis_title="",
            title="",
            showlegend=False
        )
        return fig

    def get_fig_participants(self, years=None, continent=None):
        l_country = self.get_list_country(years, continent)
        l_nocs = self.get_noc_of_list_country(l_country)

        bars = []
        for noc in l_nocs:
            participant = self.get_number_participant(years, noc)
            bars.append(
                go.Bar(name=self.get_country_of_noc(noc), y=[
                       participant], x=[self.get_country_of_noc(noc)])
            )

        fig = go.Figure(data=bars)

        fig.update_layout(
            xaxis_title="Nombre de participant par pays",
            showlegend=False,
        )
        return fig

    def get_fig_repartition_sports(self, years=None, country=None, continent=None):

        data = self.data
        if years is not None:
            data = data[data["Year"].isin(years)]

        if country is not None:
            data = data[data["NOC"] == self.get_noc_of_country(country)]
        elif continent is not None:
            data = data[data["NOC"].isin(self.get_noc_of_list_country(
                self.get_list_country(years, continent)))]

        men_data = data[data['Sex'] == 'M']
        women_data = data[data['Sex'] == 'F']

        men_sport_participation = men_data['Sport'].value_counts(
        ).reset_index()
        men_sport_participation.columns = ['Sport', "Nombre d'athlètes Homme"]

        women_sport_participation = women_data['Sport'].value_counts(
        ).reset_index()
        women_sport_participation.columns = [
            'Sport', "Nombre d'athlètes Femme"]

        merged_sport_participation = pd.merge(
            men_sport_participation, women_sport_participation, on='Sport', how='outer').fillna(0)

        bar_chart = go.Figure()

        bar_chart.add_trace(go.Bar(x=merged_sport_participation['Sport'],
                                   y=merged_sport_participation["Nombre d'athlètes Homme"],
                                   name='Men'))

        bar_chart.add_trace(go.Bar(x=merged_sport_participation['Sport'],
                                   y=merged_sport_participation["Nombre d'athlètes Femme"],
                                   name='Women'))

        bar_chart.update_layout(
            title="Participation au Sport - Nombre d'athlètes dans chaque sport (Homme et femme)",
            xaxis=dict(title='Sport'),
            yaxis=dict(title="Nombre d'Athlètes"),
            barmode='stack'
        )
        return bar_chart
