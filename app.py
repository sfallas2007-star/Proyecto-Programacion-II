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
