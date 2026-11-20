# ============================================================
# 1. LIBRERÍAS DEL PROYECTO
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
# 2. CARGA Y PREPARACIÓN DE LOS DATOS
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
    labels=[
        "81–84 años",
        "85–88 años",
        "89 años o más"
    ]
)


# ============================================================
# 3. VARIABLES DEL ANÁLISIS DE CORRELACIONES
# ============================================================

variables_correlaciones = [
    "peso",
    "altura",
    "cintura",
    "cadera",
    "tobillo",
    "rodilla"
]


# ============================================================
# 4. INTERFAZ DE LA APLICACIÓN
# ============================================================

app_ui = ui.page_sidebar(

    # --------------------------------------------------------
    # BARRA LATERAL: FILTROS GENERALES
    # --------------------------------------------------------

    ui.sidebar(

        ui.h4("Filtros generales"),

        # FILTRO DE SEXO

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

        # FILTRO DE EDAD

        ui.input_select(
            "edad",
            "Seleccionar grupo de edad:",
            choices={
                "Todos": "Todos",
                "81–84 años": "81–84 años",
                "85–88 años": "85–88 años",
                "89 años o más": "89 años o más"
            },
            selected="Todos"
        )

    ),


    # ========================================================
    # PESTAÑAS DE LA APLICACIÓN
    # ========================================================

    ui.navset_tab(

        # ----------------------------------------------------
        # PESTAÑA 0: CONTEXTO DEL PROYECTO
        # ----------------------------------------------------

        ui.nav_panel(

            "Contexto",

            ui.h2("Perfil antropométrico en adultos mayores"),

            ui.h4("Estudio ENASEM"),

            ui.hr(),

            ui.layout_columns(

                ui.card(

                    ui.card_header("Sobre el proyecto"),

                    ui.p(
                        "Esta aplicación fue desarrollada con el fin de "
                        "explorar y analizar información antropométrica proveniente "
                        "de la Encuesta Nacional sobre Salud y Envejecimiento "
                        "en México (ENASEM)."
                    ),

                    ui.p(
                        "La ENASEM es un estudio longitudinal que investiga "
                        "el proceso de envejecimiento, el estado de salud, la "
                        "mortalidad y diversos factores sociodemográficos de "
                        "la población adulta mayor mexicana."
                    )
                ),

                ui.card(

                    ui.card_header("Descripción del conjunto de datos"),

                    ui.tags.ul(

                        ui.tags.li("93 observaciones de adultos mayores."),

                        ui.tags.li(
                            "11 variables originales de carácter "
                            "antropométrico y sociodemográfico."
                        ),

                        ui.tags.li(
                            "Información sobre sexo, edad, escolaridad y "
                            "medidas corporales."
                        ),

                        ui.tags.li(
                            "Variables antropométricas como peso, altura, "
                            "cintura, cadera, rodilla y tobillo."
                        )
                    )
                ),

                col_widths=[6, 6]

            ),

            ui.hr(),

            ui.layout_columns(

                ui.card(

                    ui.card_header("Indicadores construidos"),

                    ui.tags.ul(

                        ui.tags.li(
                            "ICC = Perímetro de cintura / Perímetro de cadera"
                        ),

                        ui.tags.li(
                            "IMC = Peso (kg) / Altura² (m²)"
                        ),

                        ui.tags.li(
                            "ICE = Perímetro de cintura / Estatura"
                        )
                    )

                ),

                ui.card(

                    ui.card_header("¿Cómo utilizar la aplicación?"),

                    ui.tags.ol(

                        ui.tags.li(
                            "Seleccione filtros de sexo y grupo de edad en la barra lateral."
                        ),

                        ui.tags.li(
                            "Navegue entre las diferentes pestañas para explorar los análisis."
                        ),

                        ui.tags.li(
                            "Interactúe con los gráficos para visualizar información detallada."
                        ),

                        ui.tags.li(
                            "Compare resultados entre diferentes grupos de individuos."
                        )
                    )

                ),

                col_widths=[6, 6]

            ),

            ui.hr(),

            ui.h3("Preguntas que responde la aplicación"),

            ui.layout_columns(

                ui.card(
                    ui.card_header("Pregunta 1"),
                    ui.p(
                        "¿Existen diferencias en la relación "
                        "cintura-cadera entre hombres y mujeres?"
                    )
                ),

                ui.card(
                    ui.card_header("Pregunta 2"),
                    ui.p(
                        "¿Qué relación existe entre el perímetro de cintura "
                        "y el perímetro de cadera en los adultos mayores?"
                    )
                ),

                ui.card(
                    ui.card_header("Pregunta 3"),
                    ui.p(
                        "¿Cómo varía el perímetro de cadera entre los "
                        "distintos grupos de edad?"
                    )
                ),

                col_widths=[4, 4, 4]

            ),

            ui.layout_columns(

                ui.card(
                    ui.card_header("Pregunta 4"),
                    ui.p(
                        "¿Existen diferencias en el perímetro de cadera "
                        "entre hombres y mujeres considerando sus grupos de edad?"
                    )
                ),

                ui.card(
                    ui.card_header("Pregunta 5"),
                    ui.p(
                        "¿Qué relación existe entre el índice de masa corporal "
                        "(IMC) y la relación cintura-estatura (ICE)?"
                    )
                ),

                ui.card(
                    ui.card_header("Pregunta 6"),
                    ui.p(
                        "¿Qué patrones de correlación existen entre las "
                        "diferentes medidas antropométricas?"
                    )
                ),

                col_widths=[4, 4, 4]

            )

        ),

        # ----------------------------------------------------
        # PESTAÑA 1: ÍNDICE CINTURA-CADERA
        # ----------------------------------------------------

        ui.nav_panel(

            "índice cintura-cadera",

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

        # ----------------------------------------------------
        # PESTAÑA 5: RELACIÓN ENTRE CINTURA Y CADERA
        # ----------------------------------------------------

        ui.nav_panel(

            "Relación cintura-cadera",

            ui.h4("Pregunta de investigación"),

            ui.p(
                "¿Qué relación existe entre el perímetro de cintura "
                "y el perímetro de cadera en los adultos mayores?"
            ),

            ui.hr(),

            ui.h4("Configuración del análisis"),

            ui.card(

                ui.input_select(
                    "metodo",
                    "Seleccionar método de correlación:",
                    choices={
                        "pearson": "Pearson",
                        "spearman": "Spearman"
                    },
                    selected="pearson"
                ),

                ui.output_text("metodo_actual")

            ),

            ui.hr(),

            ui.h4("Diagrama de dispersión por sexo"),

            ui.output_plot("dispersion"),

            ui.hr(),

            ui.h4("Resultados del análisis de correlación"),

            ui.output_table("resultado_correlacion")

        ),


        # ----------------------------------------------------
        # PESTAÑA 6: MATRIZ DE CORRELACIONES
        # ----------------------------------------------------

        ui.nav_panel(

            "Matriz de correlaciones",

            ui.h4("Pregunta de investigación"),

            ui.p(
                "¿Qué patrones de correlación existen entre las diferentes "
                "medidas antropométricas de los individuos?"
            ),

            ui.hr(),

            ui.h4("Matriz de correlaciones"),

            ui.output_plot("heatmap"),

            ui.hr(),

            ui.p(
                "Interpretación: los coeficientes cercanos a -1 indican "
                "correlaciones negativas fuertes; los cercanos a 1 indican "
                "correlaciones positivas fuertes; y los cercanos a 0 "
                "indican relaciones lineales débiles."
            ),

            ui.p(
                "Fuente: elaboración propia. Coeficiente de correlación "
                "de Pearson."
            ),

            ui.hr(),

            ui.h4("Tabla de coeficientes de correlación"),

            ui.output_table("tabla_correlaciones"),

            ui.hr(),

            ui.h4("Filtro adicional de zona de residencia"),

            ui.input_select(
                "zona_correlaciones",
                "Seleccionar zona:",
                choices={
                    "Todas": "Todas",
                    "1": "Urbana",
                    "0": "Rural"
                },
                selected="Todas"
            )

        )

    ),

    title="Perfil antropométrico en adultos mayores"

)


# ============================================================
# 5. FUNCIONES DEL SERVIDOR
# ============================================================

def server(input, output, session):


    # ========================================================
    # 5.1. FILTROS GENERALES DE SEXO Y EDAD
    # ========================================================

    @reactive.calc
    def datos_filtrados():

        datos = df.copy()

        # FILTRO DE SEXO

        sexo_seleccionado = input.sexo()

        if sexo_seleccionado != "Todos":

            datos = datos[
                datos["sexo"] == sexo_seleccionado
            ]


        # FILTRO DE GRUPO DE EDAD

        edad_seleccionada = input.edad()

        if edad_seleccionada != "Todos":

            datos = datos[
                datos["grupo_edad"] == edad_seleccionada
            ]

        return datos.copy()


    # ========================================================
    # 5.2. INDICADORES DEL ÍNDICE CINTURA-CADERA
    # ========================================================

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


    # ========================================================
    # 5.3. GRÁFICO 1: ÍNDICE CINTURA-CADERA
    # ========================================================

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


    # ========================================================
    # 5.4. GRÁFICO 2: PERÍMETRO DE CADERA POR EDAD
    # ========================================================

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

    # ========================================================
    # 5.5. GRÁFICO 3: CADERA SEGÚN SEXO Y GRUPO DE EDAD
    # ========================================================


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

            category_orders={
                "grupo_edad": [
                    "81–84 años",
                    "85–88 años",
                    "89 años o más"
                ]
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


    # ========================================================
    # 5.6. GRÁFICO 4: RELACIÓN ENTRE IMC E ICE
    # ========================================================

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


    # ========================================================
    # 5.7. GRÁFICO 5: RELACIÓN ENTRE CINTURA Y CADERA
    # ========================================================


    # --------------------------------------------------------
    # PREPARACIÓN DE LOS DATOS
    # --------------------------------------------------------

    @reactive.calc
    def datos_grafico_cintura_cadera():

        datos = datos_filtrados()

        return datos[
            ["cintura", "cadera", "sexo"]
        ].copy()


    # --------------------------------------------------------
    # DIAGRAMA DE DISPERSIÓN Y LÍNEAS DE TENDENCIA
    # --------------------------------------------------------

    @render.plot
    def dispersion():

        datos = datos_grafico_cintura_cadera()

        fig, ax = plt.subplots(figsize=(10, 6))

        colores = {
            "Hombre": "#4472C4",
            "Mujer": "#ED7D31"
        }

        for grupo, color in colores.items():

            grupo_datos = datos[
                datos["sexo"] == grupo
            ].dropna(
                subset=["cintura", "cadera"]
            )

            if grupo_datos.empty:
                continue

            ax.scatter(
                grupo_datos["cintura"],
                grupo_datos["cadera"],
                color=color,
                label=grupo,
                alpha=0.7,
                s=45
            )

            if grupo_datos["cintura"].nunique() >= 2:

                x = grupo_datos["cintura"].to_numpy()
                y = grupo_datos["cadera"].to_numpy()

                pendiente, intercepto = np.polyfit(x, y, 1)

                x_linea = np.linspace(
                    x.min(),
                    x.max(),
                    100
                )

                y_linea = pendiente * x_linea + intercepto

                ax.plot(
                    x_linea,
                    y_linea,
                    color=color,
                    linewidth=2
                )

        ax.set_title(
            "Relación entre el perímetro de cintura y cadera",
            fontsize=14,
            fontweight="bold",
            color="#17365D"
        )

        ax.set_xlabel(
            "Perímetro de cintura (cm)",
            fontsize=11
        )

        ax.set_ylabel(
            "Perímetro de cadera (cm)",
            fontsize=11
        )

        ax.legend(title="Sexo")
        ax.grid(alpha=0.25)

        fig.tight_layout()

        return fig


    # --------------------------------------------------------
    # CÁLCULO Y PRESENTACIÓN DE LAS CORRELACIONES
    # --------------------------------------------------------

    @render.table
    def resultado_correlacion():

        # Obtener los datos que ya incluyen los filtros generales
        datos = datos_grafico_cintura_cadera().copy()

        # Leer el método seleccionado directamente del selector
        metodo = str(input.metodo()).strip().lower()

        # Seleccionar la función estadística
        if metodo == "pearson":

            funcion = stats.pearsonr
            nombre_metodo = "Pearson"

        elif metodo == "spearman":

            funcion = stats.spearmanr
            nombre_metodo = "Spearman"

        else:

            raise ValueError(
                f"Método no reconocido: {metodo}"
            )

        # Separar los datos en tres grupos
        grupos = {

            "Total": datos,

            "Hombres": datos[
                datos["sexo"] == "Hombre"
            ],

            "Mujeres": datos[
                datos["sexo"] == "Mujer"
            ]

        }

        resultados = []

        # Calcular la correlación para cada grupo
        for nombre, grupo in grupos.items():

            # Eliminar datos faltantes
            grupo = grupo[
                ["cintura", "cadera"]
            ].dropna()

            x = grupo["cintura"]
            y = grupo["cadera"]

            # Verificar que existan suficientes datos y variación
            if (
                len(grupo) >= 2
                and x.nunique() >= 2
                and y.nunique() >= 2
            ):

                # Calcular usando el método seleccionado
                coeficiente, valor_p = funcion(
                    x.to_numpy(),
                    y.to_numpy()
                )

            else:

                coeficiente = np.nan
                valor_p = np.nan

            # Guardar los resultados
            resultados.append({

                "Grupo": nombre,

                "Método utilizado": nombre_metodo,

                "Coeficiente": (
                    f"{coeficiente:.4f}"
                    if pd.notna(coeficiente)
                    else "No disponible"
                ),

                "Valor p": (
                    f"{valor_p:.2e}"
                    if pd.notna(valor_p)
                    else "No disponible"
                )

            })

        return pd.DataFrame(resultados)


    # --------------------------------------------------------
    # MOSTRAR EL MÉTODO SELECCIONADO
    # --------------------------------------------------------

    @render.text
    def metodo_actual():

        metodo = str(input.metodo()).strip().lower()

        if metodo == "pearson":

            return "Método seleccionado: Pearson"

        elif metodo == "spearman":

            return "Método seleccionado: Spearman"

        else:

            return "Método no reconocido"


    # ========================================================
    # 5.8. GRÁFICO 6: MATRIZ DE CORRELACIONES
    # ========================================================


    # --------------------------------------------------------
    # FILTRAR LOS DATOS SEGÚN LA ZONA DE RESIDENCIA
    # --------------------------------------------------------

    @reactive.calc
    def datos_matriz_correlaciones():

        datos = datos_filtrados().copy()

        zona_seleccionada = input.zona_correlaciones()

        if zona_seleccionada != "Todas":

            datos = datos[
                datos["urbano"] == int(zona_seleccionada)
            ]

        return datos


    # --------------------------------------------------------
    # CALCULAR LA MATRIZ DE CORRELACIONES
    # --------------------------------------------------------

    @reactive.calc
    def matriz_correlaciones():

        datos = datos_matriz_correlaciones()

        return datos[
            variables_correlaciones
        ].corr(
            method="pearson"
        )


    # --------------------------------------------------------
    # GENERAR EL MAPA DE CALOR
    # --------------------------------------------------------

    @render.plot
    def heatmap():

        correlaciones = matriz_correlaciones()

        fig, ax = plt.subplots(figsize=(10, 7))

        sns.heatmap(

            correlaciones,

            annot=True,

            cmap="coolwarm",

            fmt=".2f",

            vmin=-1,

            vmax=1,

            center=0,

            linewidths=0.5,

            square=True,

            ax=ax

        )

        ax.set_title(
            "Matriz de correlaciones de las medidas antropométricas"
        )

        fig.tight_layout()

        return fig


    # --------------------------------------------------------
    # TABLA DE COEFICIENTES DE CORRELACIÓN
    # --------------------------------------------------------

    @render.table
    def tabla_correlaciones():

        return matriz_correlaciones().round(3)


# ============================================================
# 6. EJECUCIÓN DE LA APLICACIÓN
# ============================================================

app = App(app_ui, server)