import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_echarts import st_echarts, JsCode
import datetime
import math
import random
import base64

import os

def get_base64_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Rutas a los logos
LOGO_PESTANA = os.path.join(os.path.dirname(__file__), "Logo_pestaña.png")
LOGO_SIDEBAR = os.path.join(os.path.dirname(__file__), "logo.png")

st.set_page_config(page_title="Selligent Labs", page_icon=LOGO_PESTANA if os.path.exists(LOGO_PESTANA) else "📊", layout="wide")

logo_b64 = get_base64_bin_file(LOGO_SIDEBAR)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Fondo principal ── */
.stApp { background-color: #FFFEFF; }

/* ── Sidebar fondo ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background-color: #093134 !important;
}

/* ── Todo el texto del sidebar en blanco ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

/* ── Título del sidebar ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important; font-weight: 700; letter-spacing: 0.04em;
}

/* ── Etiqueta encima del radio ── */
[data-testid="stSidebar"] .stRadio > label {
    color: #7ab5b8 !important; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;
}

/* ── Items del menú ── */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {
    padding: 4px 10px !important; border-radius: 7px !important; margin: 1px 0 !important;
    font-size: 13px !important; font-weight: 500 !important; color: #ffffff !important;
    transition: background 0.2s ease !important; cursor: pointer !important;
    text-transform: none !important; letter-spacing: normal !important;
    display: flex !important; align-items: center !important; gap: 8px !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background-color: #0d4a4e !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked),
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
    background-color: #0e5558 !important; color: #ffffff !important;
    font-weight: 600 !important; box-shadow: inset 3px 0 0 #5ec4c8 !important;
}

/* ── Keyframes para iconos del menú ── */
@keyframes iconPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.65; transform: scale(0.92); }
}
@keyframes iconFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
}
@keyframes iconGlow {
    0%, 100% { filter: drop-shadow(0 0 3px #5ec4c8); }
    50% { filter: drop-shadow(0 0 7px #5ec4c8) brightness(1.3); }
}

/* ── Ocultar SOLO el toggle/círculo nativo, NO el texto ── */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label input[type="radio"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label [data-baseweb="radio"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ── Icono SVG via ::before para cada item del menú ── */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    animation: iconFloat 3s ease-in-out infinite;
}
/* Icono Inicio (casa) */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(1)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c8e8ea' stroke-width='1.8' stroke-linejoin='round'%3E%3Cpath d='M3 11.5L12 3l9 8.5V21h-6v-5.5H9V21H3V11.5z'/%3E%3C/svg%3E");
    animation-duration: 4s;
}
/* Icono Análisis de Ventas (gráfica de barras) */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(2)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23c8e8ea'%3E%3Crect x='3' y='11' width='4' height='10' rx='1'/%3E%3Crect x='10' y='5' width='4' height='16' rx='1'/%3E%3Crect x='17' y='8' width='4' height='13' rx='1'/%3E%3C/svg%3E");
    animation-duration: 2.5s;
    animation-delay: 0.3s;
}
/* Icono Modelo (cerebro/nodo neural) */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:nth-child(3)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c8e8ea' stroke-width='1.6' stroke-linecap='round'%3E%3Ccircle cx='12' cy='9' r='6'/%3E%3Cline x1='8' y1='21' x2='16' y2='21'/%3E%3Cline x1='12' y1='15' x2='12' y2='21'/%3E%3Ccircle cx='12' cy='9' r='2.2' fill='%235ec4c8' stroke='none'/%3E%3C/svg%3E");
    animation: iconPulse 3s ease-in-out infinite;
    animation-delay: 0.6s;
}
/* Icono activo — glow turquesa */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked)::before {
    animation: iconGlow 2s ease-in-out infinite !important;
}

/* ── Menú desplegable: opciones en blanco ── */
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[data-baseweb="option"],
[data-baseweb="option"] *,
[role="listbox"] *,
[role="option"],
[role="option"] * {
    color: #ffffff !important;
    background-color: #0a3d40 !important;
}
[data-baseweb="option"]:hover,
[data-baseweb="option"]:hover *,
[aria-selected="true"],
[aria-selected="true"] * {
    background-color: #0e5558 !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr { border-color: #1a5558 !important; opacity: 0.6; }
[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #0d4a4e; border-radius: 4px; }

/* ══════════════════════════════════════════
   SELECTBOXES Y MULTISELECTS ESTILIZADOS
   ══════════════════════════════════════════ */

/* Contenedor del selectbox */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: #093134 !important;
    border: 1.5px solid #1a6b70 !important;
    border-radius: 10px !important;
    color: #e0f4f5 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stMultiSelect"] > div > div:hover {
    border-color: #5ec4c8 !important;
    box-shadow: 0 0 0 3px #5ec4c820 !important;
}

/* Texto dentro del select */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-testid="stMultiSelect"] span,
[data-testid="stMultiSelect"] p {
    color: #e0f4f5 !important;
    font-weight: 500 !important;
}

/* Flecha del dropdown */
[data-testid="stSelectbox"] svg,
[data-testid="stMultiSelect"] svg {
    fill: #5ec4c8 !important;
    color: #5ec4c8 !important;
}

/* Etiqueta encima del select */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
    color: #093134 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* Texto seleccionado visible dentro del select */
[data-testid="stSelectbox"] div[data-baseweb="select"] span,
[data-testid="stSelectbox"] div[data-baseweb="select"] div,
[data-testid="stSelectbox"] div[data-baseweb="select"] p,
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stSelectbox"] input,
[data-testid="stMultiSelect"] div[data-baseweb="select"] span,
[data-testid="stMultiSelect"] div[data-baseweb="select"] div,
[data-testid="stMultiSelect"] div[data-baseweb="select"] p,
[data-testid="stMultiSelect"] [data-baseweb="select"] *,
[data-testid="stMultiSelect"] input {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Placeholder text */
[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="select-placeholder"],
[data-testid="stMultiSelect"] [data-baseweb="select"] [data-baseweb="select-placeholder"] {
    color: #a0cfd1 !important;
}
[data-testid="stSelectbox"] ul,
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {
    background-color: #0a3d40 !important;
    border: 1px solid #1a6b70 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-baseweb="menu"] li,
[data-baseweb="option"] {
    background-color: #0a3d40 !important;
    color: #c8e6e8 !important;
    font-size: 14px !important;
    border-radius: 6px !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover {
    background-color: #0e5558 !important;
    color: #ffffff !important;
}

/* Tags del multiselect */
[data-baseweb="tag"] {
    background-color: #0e5558 !important;
    border-radius: 6px !important;
    border: 1px solid #5ec4c8 !important;
}
[data-baseweb="tag"] span { color: #e0f4f5 !important; font-weight: 500 !important; }
[data-baseweb="tag"] button svg { fill: #5ec4c8 !important; }

/* ── Títulos principales ── */
.stApp h1 { color: #093134 !important; font-weight: 800 !important; }
.stApp h2, .stApp h3 { color: #093134 !important; font-weight: 700 !important; }
.stApp p, .stApp li { color: #2a4a4c !important; }

/* ── Divider ── */
hr { border-color: #d0e8e9 !important; }

/* ── Info/warning boxes ── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── Métricas nativas ── */
[data-testid="metric-container"] {
    background: #f0fafa; border-radius: 12px;
    padding: 12px 16px; border: 1px solid #b0d8da;
}

/* ── Botones ── */
.stButton > button {
    background-color: #093134 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    background-color: #0e5558 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px #09313440 !important;
}
/* ── Texto siempre blanco dentro de cualquier botón ── */
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
}
/* ── Botón de eliminar análisis (❌) ── */
[data-testid="stHorizontalBlock"] .stButton > button:has(p:-webkit-any(*, *)) {
    background-color: #093134 !important;
}
/* Botón ❌ — forzar texto claro para todos los botones secundarios */ 
.stButton > button:not([kind="primary"]) p { color: #ffffff !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1.5px solid #c0dfe0 !important;
    border-radius: 12px !important;
    background: #f5fafa !important;
}
[data-testid="stExpander"] summary {
    color: #093134 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)




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

from inicio import mostrar_inicio
from analisis import mostrar_analisis
from modelo import mostrar_modelo

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
