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
    

    def get_config(self) -> dict:
        with open("config/config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config


    def get_number_of_(self, sex, year=None, country=None, continent=None ):
        df_men = self.data[self.data["Sex"] == sex]
        if year is not None:
            df_men = df_men[df_men["Year"] == year]
        
        if country is not None and continent is None:
            df_men = df_men[df_men["NOC"] == self.get_noc_of_country(country)]
        elif continent is not None:
            df_men_sub = df_men.copy()
            for noc in self.config[continent]:
                df_men = pd.concat([df_men, df_men_sub[df_men_sub["NOC"] == noc]])
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


    def get_noc_of_country(self, country):
        noc =  self.regions.loc[self.regions["region"] == country, "NOC"]
        return noc.iloc[0]

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
        bars.append(go.Bar(name="% of men", x=["Homme"], y=[100*nb_man/(max(nb_man+nb_woman, 1))]))
        bars.append(go.Bar(name="% of women", x=["Femme"], y=[100*nb_woman/(max(nb_man+nb_woman, 1))]))
        
        fig = go.Figure(data=bars)

        fig.update_layout(
            barmode='stack',
            xaxis_title="Répartition Homme Femme", yaxis_title="%",
            title= "",
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
            df_medal = pd.concat([self.data[self.data["Year"]==year], df_medal])
        if noc is not None:
            df_medal = df_medal[df_medal["NOC"] == noc]
        print(df_medal)
        res = {"Or":0, "Argent":0, "Bronze":0}
        #df_medal.to_csv("data/test_france.csv")
        df_medal = df_medal.groupby(["Event", "Medal"], as_index = False).agg("count")

        res["Or"] = len(df_medal[df_medal["Medal"] == "Gold"])
        res["Argent"] = len(df_medal[df_medal["Medal"] == "Silver"])
        res["Bronze"] = len(df_medal[df_medal["Medal"] == "Bronze"])
        print("medals : ", res)
        return res

    def get_fig_medals(self, years=None, country=None, continent=None):
        medals = Counter({"Or":0, "Argent":0, "Bronze":0})
        if country is not None:
            medals = Counter(self.get_medals(years, self.get_noc_of_country(country)))
        elif continent is not None:
            for noc in self.config[continent]:
                medals += Counter(self.get_medals(years, noc))
        else:
            medals = Counter(self.get_medals(years))
        print("les médailles : ", medals)
        fig = go.Figure(data=go.Bar(x=["Or", "Argent", "Bronze"], y=[4, 1, 2], marker=dict(color =["#FFD700", "#C0C0C0", "#614e1a"])))

        fig.update_layout(
            barmode='stack',
            xaxis_title="Types de médailles", yaxis_title="Nombre de médailles",
            title= "",
            showlegend=False
        )
        return fig

