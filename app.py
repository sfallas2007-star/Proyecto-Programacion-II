# ============================================================
# LIBRERÍAS DEL PROYECTO
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
from pathlib import Path
# ============================================================
# 1. CARGA Y PREPARACIÓN DE LOS DATOS
# ============================================================
ruta = Path(__file__).parent / "antropometria.csv"
df = pd.read_csv(ruta)

# Codificación de sexo
df["sexo"] = df["sexo"].map({
    1: "Hombre",
    2: "Mujer"
})

# Índice cintura-cadera
df["ICC"] = df["cintura"] / df["cadera"]

# Índice de masa corporal
df["altura_m"] = df["altura"] / 100
df["IMC"] = df["peso"] / (df["altura_m"] ** 2)

# Índice cintura-estatura
df["ICE"] = df["cintura"] / df["altura"]

# Grupos de edad
df["grupo_edad"] = pd.cut(
    df["edad"],
    bins=[80, 84, 88, float("inf")],
    labels=["81–84 años", "85–88 años", "89 años o más"]
)


# ============================================================
# 2. INTERFAZ DE LA APLICACIÓN
# ============================================================

app_ui = ui.page_sidebar(

    ui.sidebar(
        ui.h4("Filtros"),
        ui.input_select(
            "sexo",
            "Seleccionar sexo:",
            choices={
                "Todos": "Todos",
                "Hombre": "Hombre",
                "Mujer": "Mujer"
            },
            selected="Todos"
        ),
    ),

    ui.navset_tab(

        # ----------------------------------------------------
        # PESTAÑA 1: ÍNDICE CINTURA-CADERA
        # ----------------------------------------------------

        ui.nav_panel(
            "Relación cintura-cadera",

            ui.h4("Pregunta de investigación"),
            ui.p(
                "¿Existen diferencias en la relación cintura-cadera "
                "entre hombres y mujeres?"
            ),

            ui.hr(),

            ui.h4("Indicadores generales"),

            ui.layout_columns(

                ui.card(
                    ui.card_header("Observaciones"),
                    ui.output_text("n_obs")
                ),

                ui.card(
                    ui.card_header("Media del ICC"),
                    ui.output_text("media_icc")
                ),

                ui.card(
                    ui.card_header("Mediana del ICC"),
                    ui.output_text("mediana_icc")
                ),

                ui.card(
                    ui.card_header("Desviación estándar"),
                    ui.output_text("sd_icc")
                ),

                col_widths=[3, 3, 3, 3]
            ),

            ui.hr(),

            ui.h4("Distribución del índice cintura-cadera"),

            output_widget("grafico_icc"),

            ui.p(
                "El gráfico permite comparar la distribución del índice "
                "cintura-cadera entre hombres y mujeres."
            )
        ),

        # ----------------------------------------------------
        # PESTAÑA 2: PERÍMETRO DE CADERA POR EDAD
        # ----------------------------------------------------

        ui.nav_panel(
            "Perímetro de cadera por edad",

            ui.h4("Pregunta de investigación"),
            ui.p(
                "¿Cómo varía el perímetro de cadera entre los distintos "
                "grupos de edad de los adultos mayores?"
            ),

            ui.hr(),

            ui.h4("Distribución del perímetro de cadera"),

            output_widget("grafico_cadera"),

            ui.p(
                "El gráfico permite comparar la distribución del "
                "perímetro de cadera entre los diferentes grupos de edad."
            )
        ), 

        # ----------------------------------------------------
        # PESTAÑA 3: CADERA SEGÚN SEXO Y EDAD
        # ----------------------------------------------------

        ui.nav_panel(

            "Cadera por sexo y edad",

            ui.h4("Pregunta de investigación"),

            ui.p(
                "¿Existen diferencias en el perímetro de cadera "
                "entre hombres y mujeres, considerando sus grupos de edad?"
            ),

            ui.hr(),

            ui.h4("Perímetro de cadera según sexo y grupo de edad"),

            output_widget("grafico_cadera_sexo"),

            ui.p(
                "El gráfico compara la distribución del perímetro "
                "de cadera entre hombres y mujeres dentro de cada grupo de edad."
            )

        ),

        # ----------------------------------------------------
        # PESTAÑA 4: RELACIÓN ENTRE IMC E ICE
        # ----------------------------------------------------

        ui.nav_panel(

            "Relación IMC e ICE",

            ui.h4("Pregunta de investigación"),

            ui.p(
                "¿Qué relación existe entre el índice de masa corporal "
                "(IMC) y la relación cintura-estatura (ICE)?"
            ),

            ui.hr(),

            ui.h4("Diagrama de dispersión"),

            output_widget("grafico_imc_ice"),

            ui.p(
                "El gráfico muestra la relación entre el IMC y el índice "
                "cintura-estatura, diferenciando a los individuos según sexo."
            )

        ),
    ),

    title="Perfil antropométrico en adultos mayores",

)


# ============================================================
# 3. FUNCIONES DEL SERVIDOR
# ============================================================

def server(input, output, session):

    # Filtro compartido por ambos gráficos

    @reactive.calc
    def datos_filtrados():

        sexo_seleccionado = input.sexo()

        if sexo_seleccionado == "Todos":
            return df.copy()

        return df[df["sexo"] == sexo_seleccionado].copy()


    # --------------------------------------------------------
    # INDICADORES DEL ÍNDICE CINTURA-CADERA
    # --------------------------------------------------------

    @render.text
    def n_obs():
        return f"{len(datos_filtrados())}"

    @render.text
    def media_icc():
        return f"{datos_filtrados()['ICC'].mean():.3f}"

    @render.text
    def mediana_icc():
        return f"{datos_filtrados()['ICC'].median():.3f}"

    @render.text
    def sd_icc():
        return f"{datos_filtrados()['ICC'].std():.3f}"


    # --------------------------------------------------------
    # GRÁFICO 1: RELACIÓN CINTURA-CADERA
    # --------------------------------------------------------

    @render_widget
    def grafico_icc():

        datos = datos_filtrados()

        fig = px.box(
            datos,
            x="sexo",
            y="ICC",
            color="sexo",
            points="all",
            hover_data=["cintura", "cadera", "edad"],
            color_discrete_map={
                "Hombre": "#1769AA",
                "Mujer": "#E67E22"
            },
            labels={
                "sexo": "Sexo",
                "ICC": "Índice cintura-cadera",
                "cintura": "Perímetro de cintura",
                "cadera": "Perímetro de cadera",
                "edad": "Edad"
            },
            title="Índice cintura-cadera según sexo"
        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            xaxis_title="Sexo",
            yaxis_title="Índice cintura-cadera",
            showlegend=False
        )

        fig.update_traces(
            marker=dict(size=8)
        )

        return fig


    # --------------------------------------------------------
    # GRÁFICO 2: PERÍMETRO DE CADERA POR GRUPO DE EDAD
    # --------------------------------------------------------

    @render_widget
    def grafico_cadera():

        datos = datos_filtrados()

        fig = px.box(
            datos,
            x="grupo_edad",
            y="cadera",
            color="grupo_edad",
            points="all",
            hover_data=["edad", "sexo"],
            category_orders={
                "grupo_edad": [
                    "81–84 años",
                    "85–88 años",
                    "89 años o más"
                ]
            },
            color_discrete_map={
                "81–84 años": "#1769AA",
                "85–88 años": "#E67E22",
                "89 años o más": "#269B72"
            },
            labels={
                "grupo_edad": "Grupo de edad",
                "cadera": "Perímetro de cadera (cm)",
                "edad": "Edad",
                "sexo": "Sexo"
            },
            title="Perímetro de cadera según grupo de edad"
        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            xaxis_title="Grupo de edad",
            yaxis_title="Perímetro de cadera (cm)",
            showlegend=False
        )

        fig.update_traces(
            marker=dict(size=8)
        )

        return fig

        # --------------------------------------------------------
    # GRÁFICO 3: CADERA SEGÚN SEXO Y GRUPO DE EDAD
    # --------------------------------------------------------

    @render_widget
    def grafico_cadera_sexo():

        datos = datos_filtrados()

        fig = px.box(

            datos,

            x="grupo_edad",
            y="cadera",
            color="sexo",

            points="all",

            hover_data=["edad"],

            color_discrete_map={
                "Hombre": "#6495ED",
                "Mujer": "#FF69B4"
            },

            labels={
                "grupo_edad": "Grupo de edad",
                "cadera": "Perímetro de cadera (cm)",
                "sexo": "Sexo"
            },

            title="Perímetro de cadera según sexo y grupo de edad"

        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            xaxis_title="Grupo de edad",
            yaxis_title="Perímetro de cadera (cm)"
        )

        fig.update_traces(
            marker=dict(size=8)
        )

        return fig

    # --------------------------------------------------------
    # GRÁFICO 4: RELACIÓN IMC E ICE
    # --------------------------------------------------------

    @render_widget
    def grafico_imc_ice():

        datos = datos_filtrados()

        fig = px.scatter(

            datos,

            x="IMC",
            y="ICE",

            color="sexo",

            trendline="ols",

            hover_data=[
                "edad",
                "peso",
                "altura"
            ],

            color_discrete_map={
                "Hombre": "#4E79A7",
                "Mujer": "#E15759"
            },

            labels={
                "IMC": "Índice de masa corporal",
                "ICE": "Índice cintura-estatura",
                "edad": "Edad",
                "peso": "Peso",
                "altura": "Altura",
                "sexo": "Sexo"
            },

            title="Relación entre IMC e ICE"

        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            xaxis_title="IMC",
            yaxis_title="ICE"
        )

        return fig


# ============================================================
# 4. EJECUCIÓN DE LA APLICACIÓN
# ============================================================

app = App(app_ui, server)