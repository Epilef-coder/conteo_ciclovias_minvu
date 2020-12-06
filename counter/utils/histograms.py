import logging
from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from counter.models.data_by_comuna import DataComuna

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Histogram:
    def __init__(self, data_comuna: List[DataComuna]):
        self.info_comuna = data_comuna
        self.comunas, self.df_comunas = self.get_dataframe()

    def get_dataframe(self):
        df = pd.DataFrame()

        comunas = []
        comunas.append({'label': "TODAS", 'value': "TODAS"})

        df_comuna = []
        df_region = []
        df_date = []
        df_count = []
        df_count2 = []
        for data in self.info_comuna:

            obj = {'label': data.comuna, 'value': data.comuna}
            if obj not in comunas:
                comunas.append(obj)

            df_comuna.append(data.comuna)
            df_region.append(data.region)
            df_date.append(data.str_date)
            df_count.append(data.count_1)
            df_count2.append(data.count_2)

        df["comuna"] = df_comuna
        df["region"] = df_region
        df["date"] = df_date
        df["count"] = df_count
        df["count2"] = df_count2

        return comunas, df

    def plot_dash(self):

        df_comunas = self.df_comunas

        app = dash.Dash(__name__)
        app.layout = html.Div([
            dcc.Graph(id="graph"),
            html.P("Comunas:"),
            dcc.Dropdown(
                id="comunas",
                options=self.comunas,
                value=[self.comunas[0]["value"]],
                multi=True,
                searchable=True
            )
        ])

        @app.callback(
            Output("graph", "figure"),
            [Input("comunas", "value")])
        def display_color(comunas):

            templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]

            str_comunas = ""

            if comunas is None or comunas == []:
                data = df_comunas
                str_comunas = "todas las comunas"

            else:
                if "TODAS" in comunas:
                    data = df_comunas
                    str_comunas = "todas las comunas"

                else:
                    data = pd.DataFrame()

                    df_comuna = []
                    df_region = []
                    df_date = []
                    df_count = []
                    df_count2 = []
                    for c in comunas:
                        if str_comunas == "":
                            str_comunas = c
                        else:
                            str_comunas += " - " + c
                        df = df_comunas[df_comunas.comuna == c]
                        df_comuna += list(df["comuna"])
                        df_region += list(df["region"])
                        df_date += list(df["date"])
                        df_count += list(df["count"])
                        df_count2 += list(df["count2"])
                    data["comuna"] = df_comuna
                    data["region"] = df_region
                    data["date"] = df_date
                    data["count"] = df_count
                    data["count2"] = df_count2
            logger.info(data.head())

            fig = px.bar(data, x="date", y=["count", "count2"],
                         title="Conteo de bicicletas para {}".format(str_comunas), opacity=0.5,
                         template="plotly")

            return fig

        app.run_server(debug=True)
