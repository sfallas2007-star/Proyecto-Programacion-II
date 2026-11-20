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
