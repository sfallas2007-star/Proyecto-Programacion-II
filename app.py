
from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
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
        )
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


# ============================================================
# 4. EJECUCIÓN DE LA APLICACIÓN
# ============================================================

app = App(app_ui, server)
