import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
import datetime
import math
import random
import base64

import os

from utils.helpers import get_base64_bin_file

# Rutas a los logos
LOGO_PESTANA = os.path.join(os.path.dirname(__file__), "assets", "Logo_pestaña.png")
LOGO_SIDEBAR = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

st.set_page_config(page_title="Selligent Labs", page_icon=LOGO_PESTANA if os.path.exists(LOGO_PESTANA) else "📊", layout="wide")

logo_b64 = get_base64_bin_file(LOGO_SIDEBAR)

css_file = os.path.join(os.path.dirname(__file__), "styles", "main.css")
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)




# Menú lateral estético
st.sidebar.markdown(f"""
<div style="padding: 8px 4px 20px 4px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
        <img src="data:image/png;base64,{logo_b64}" style="height:58px; width:auto; border-radius:10px;"/>
        <span style="font-size:18px;font-weight:800;color:#ffffff;letter-spacing:0.03em;line-height:1.2;">Selligent Labs<br><span style="font-size:11px;font-weight:400;color:#5ec4c8;letter-spacing:0.08em;text-transform:uppercase;">Inteligencia para tu negocio</span></span>
    </div>
    <hr style="border:none;border-top:1px solid #7a8a6a55;margin:12px 0 16px 0;"/>
    <div style="font-size:10px;color:#a09878;text-transform:uppercase;letter-spacing:0.12em;font-weight:600;margin-bottom:8px;padding-left:4px;">Navegación</div>
</div>
""", unsafe_allow_html=True)

opcion = st.sidebar.radio("", ["Inicio", "Análisis de Ventas", "Predicción Inteligente"])

st.sidebar.markdown("""
<div style="position:fixed;bottom:32px;left:0;width:var(--sidebar-width,260px);padding:0 20px;">
    <div style="border-top:1px solid #7a8a6a44;padding-top:14px;">
        <div style="font-size:11px;color:#8a9a7a;text-align:center;line-height:1.6;">
            Hecho por Didier Moreno<br>
            <span style="color:#c8b97a;font-weight:600;">Streamlit + ECharts</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

from pages.inicio import mostrar_inicio
from pages.analisis import mostrar_analisis
from pages.modelo import mostrar_modelo

if "df" not in st.session_state:
    st.session_state.df = None
if "last_filename" not in st.session_state:
    st.session_state.last_filename = None
if "analyses" not in st.session_state:
    st.session_state.analyses = [{"id": 0, "date_col": None, "target_col": None, "cat_col": None}]
if "analysis_counter" not in st.session_state:
    st.session_state.analysis_counter = 1
if "date_cols" not in st.session_state:
    st.session_state.date_cols = []
if "num_cols" not in st.session_state:
    st.session_state.num_cols = []
if "cat_cols" not in st.session_state:
    st.session_state.cat_cols = []


if opcion == "Inicio":
    mostrar_inicio()
elif opcion == "Análisis de Ventas":
    mostrar_analisis()
elif opcion == "Predicción Inteligente":
    mostrar_modelo()
