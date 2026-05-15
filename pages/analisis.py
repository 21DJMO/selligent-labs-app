import streamlit as st
import pandas as pd
import numpy as np
import os
import hashlib
from streamlit_echarts import st_echarts, JsCode
from services.insights_engine import render_insights_section
from components.kpis import make_card
from utils.helpers import safe_pct, format_delta, icon_color

@st.cache_data
def load_data(file):
    # Creamos un directorio local para simular la persistencia de datos del servidor
    os.makedirs("data_warehouse", exist_ok=True)
    
    # Usamos el contenido del archivo para crear un identificador único (hash)
    # Así, si suben el mismo archivo, no lo procesamos dos veces
    file_content = file.getvalue()
    file_hash = hashlib.md5(file_content).hexdigest()
    csv_path = os.path.join("data_warehouse", f"dataset_{file_hash}.csv")
    
    # 1. Si el archivo ya fue procesado y convertido a CSV, lo leemos directamente (Súper rápido)
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
        
    # 2. Si no existe, es la primera vez. Lo leemos en su formato original.
    file.seek(0)
    df = None
    if file.name.endswith('.csv'):
        try:
            df = pd.read_csv(file)
            if len(df.columns) == 1 and ';' in df.columns[0]:
                file.seek(0)
                df = pd.read_csv(file, sep=';', encoding='utf-8')
                if len(df.columns) == 1:
                    file.seek(0)
                    df = pd.read_csv(file, sep=';', encoding='latin1')
        except:
            file.seek(0)
            df = pd.read_csv(file, sep=';', encoding='latin1')
    elif file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file)
        
    # 3. Guardamos el DataFrame en formato CSV limpio para futuras consultas
    if df is not None:
        df.to_csv(csv_path, index=False)
        
    return df
    
    
def mostrar_analisis():
    # ── Mini Hero para la página de Análisis ──
    st.markdown("""
    <style>
    @keyframes _grad  { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
    @keyframes _orb   { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-18px) scale(1.07)} }
    @keyframes _dot   { 0%,100%{opacity:.25} 50%{opacity:.7} }
    @keyframes _chip  { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
    </style>
    <div style="background:linear-gradient(135deg,#041e20 0%,#062527 30%,#093134 60%,#0d4a4e 85%,#145055 100%);background-size:400% 400%;animation:_grad 10s ease-in-out infinite;border-radius:22px;padding:48px 52px 42px;margin-bottom:36px;position:relative;overflow:hidden;border:1px solid rgba(94,196,200,0.25);box-shadow:0 24px 60px rgba(0,0,0,0.35),0 0 0 1px rgba(94,196,200,0.08) inset;">
      <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(94,196,200,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(94,196,200,0.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;"></div>
      <div style="position:absolute;top:-90px;right:-90px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(94,196,200,0.18) 0%,transparent 65%);animation:_orb 7s ease-in-out infinite;"></div>
      <div style="position:absolute;bottom:-100px;right:160px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,0.12) 0%,transparent 65%);animation:_orb 9s ease-in-out infinite reverse;"></div>
      <div style="position:absolute;top:40px;left:-60px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(245,158,11,0.09) 0%,transparent 65%);animation:_orb 11s ease-in-out infinite;"></div>
      <div style="position:absolute;top:28px;right:280px;width:6px;height:6px;border-radius:50%;background:#5ec4c8;animation:_dot 2.2s ease-in-out infinite;"></div>
      <div style="position:absolute;top:55px;right:310px;width:4px;height:4px;border-radius:50%;background:#7dd9dd;animation:_dot 3s ease-in-out infinite 0.4s;"></div>
      <div style="position:absolute;bottom:40px;left:200px;width:5px;height:5px;border-radius:50%;background:#6366f1;animation:_dot 2.8s ease-in-out infinite 0.8s;"></div>
      <div style="position:absolute;bottom:0;left:52px;right:52px;height:2px;background:linear-gradient(90deg,transparent,rgba(94,196,200,0.6) 30%,rgba(99,102,241,0.5) 70%,transparent);border-radius:2px;"></div>
      <div style="position:relative;z-index:1;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:22px;">
          <span class="sl-banner-badge" style="background:rgba(94,196,200,0.15);color:#7dd9dd;border-color:rgba(94,196,200,0.35);animation:_chip .5s ease both;">&#128202; Inteligencia de Negocio</span>
          <span class="sl-banner-badge" style="background:rgba(255,255,255,0.06);color:#a5b4fc;border-color:rgba(99,102,241,0.25);animation:_chip .5s .12s ease both;">&#9889; Tiempo real</span>
        </div>
        <div style="color:#fff;font-size:clamp(28px,3.8vw,42px);font-weight:900;letter-spacing:-.04em;line-height:1.1;margin-bottom:14px;">
          An&#225;lisis de <span style="color:#5ec4c8;text-shadow:0 0 28px rgba(94,196,200,0.5);">Ventas</span>
        </div>
        <div style="color:#b0d4d6;font-size:15px;font-weight:400;line-height:1.7;max-width:560px;margin-bottom:24px;">Sube tus datos y transforma n&#250;meros en <strong style="color:#5ec4c8;font-weight:700;">decisiones estrat&#233;gicas</strong> en segundos, sin necesidad de c&#243;digo.</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
          <div class="sl-banner-chip" style="animation:_chip .5s .2s ease both;">
            <span>&#128193;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">CSV &amp; Excel</span>
          </div>
          <div class="sl-banner-chip" style="animation:_chip .5s .3s ease both;">
            <span>&#129302;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">Detecci&#243;n Autom&#225;tica</span>
          </div>
          <div class="sl-banner-chip" style="animation:_chip .5s .4s ease both;">
            <span>&#128200;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">Visualizaciones Interactivas</span>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;margin-top:4px;">
      <div style="width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#062527,#0d4a4e);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(9,49,52,0.3);flex-shrink:0;">
        <svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#5ec4c8' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/><polyline points='17 8 12 3 7 8'/><line x1='12' y1='3' x2='12' y2='15'/></svg>
      </div>
      <div>
        <div style="color:#093134;font-size:20px;font-weight:900;letter-spacing:-.02em;line-height:1.1;">Carga de Datos</div>
        <div style="color:#6b9ea0;font-size:12px;font-weight:500;margin-top:2px;">Importa tu archivo para comenzar el análisis</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0fafa 0%,#e8f7f7 100%);border:1px solid #c8e8e9;border-left:4px solid #f59e0b;padding:16px 20px;border-radius:0 12px 12px 0;margin-bottom:20px;box-shadow:0 2px 8px rgba(94,196,200,0.08);">
        <div style="font-size:13px;font-weight:700;color:#093134;margin-bottom:6px;display:flex;align-items:center;gap:7px;">
          <span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:#fff8e7;border-radius:6px;border:1px solid #fde68a;">
            <svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#f59e0b' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M9 18h6'/><path d='M10 22h4'/><path d='M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .34 2.02 1.5 3.5.76.76 1.23 1.52 1.41 2.5'/></svg>
          </span>
          ¿Cómo obtengo mis datos?
        </div>
        <div style="font-size:13px;color:#4a6e70;line-height:1.6;">La mayoría de sistemas (POS, Shopify, facturación) permiten exportar ventas diarias. Busca <b style='color:#093134;'>"Exportar a Excel"</b> o <b style='color:#093134;'>"CSV"</b>.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Ver formato recomendado", expanded=False, icon=":material/description:"):
        st.markdown("""
        <div style="font-size:13.5px;color:#4a6e70;margin-bottom:12px;">
            Tu archivo debe ser similar a esta tabla. Detectamos tus columnas automáticamente, sin importar su nombre original:
        </div>
        """, unsafe_allow_html=True)
        
        df_ejemplo = pd.DataFrame({
            "Fecha": ["2023-10-01", "2023-10-02", "2023-10-03"],
            "Producto": ["Zapatos", "Camiseta", "Pantalón"],
            "Categoria": ["Calzado", "Ropa", "Ropa"],
            "Ventas": [1200.50, 450.00, 800.00],
            "Cantidad": [2, 3, 2]
        })
        st.dataframe(df_ejemplo, hide_index=True, use_container_width=True)
        
        csv_ejemplo = df_ejemplo.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Plantilla CSV",
            icon=":material/download:",
            data=csv_ejemplo,
            file_name='plantilla_ventas_ejemplo.csv',
            mime='text/csv'
        )
    
    st.markdown("""
    <div style="color:#4a6e70;font-size:13.5px;margin:20px 0 10px 0;font-weight:500;">
        Sube tu archivo (<b>CSV o Excel</b>) aquí para iniciar:
    </div>
    """, unsafe_allow_html=True)
    archivo = st.file_uploader("", type=["csv", "xlsx", "xls"])
    
    if archivo:
        if st.session_state.last_filename != archivo.name:
            df = load_data(archivo)
            if df is not None:
                st.session_state.df = df
                st.session_state.last_filename = archivo.name
                st.session_state.analyses = [{"id": 0, "date_col": None, "target_col": None, "cat_col": None}]
                st.session_state.analysis_counter = 1
                
                # 1. Detección automática inicial
                st.session_state.num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                st.session_state.cat_cols = df.select_dtypes(include=['object', 'category', 'bool', 'string']).columns.tolist()
                st.session_state.date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
                
                # 2. Heurística avanzada para Fechas y Números "Sucios"
                for col in st.session_state.cat_cols[:]:
                    muestra = df[col].dropna().astype(str).head(50)
                    if muestra.empty:
                        continue
                        
                    # Intentar detectar si es Fecha (pd.to_datetime es súper robusto con casi cualquier formato)
                    # dayfirst=False por defecto, pero inferirá bastante bien
                    fechas_detectadas = pd.to_datetime(muestra, errors='coerce')
                    if fechas_detectadas.notna().mean() > 0.5:
                        st.session_state.date_cols.append(col)
                        st.session_state.cat_cols.remove(col)
                        # Convertimos toda la columna para facilitar el uso posterior
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        continue
                        
                    # Intentar detectar si es un Número "Sucio" (ej: "$ 1,200.50" o "1,200")
                    # Quitamos signos de moneda, comas y espacios.
                    muestra_limpia = muestra.str.replace(r'[$,€£\s]', '', regex=True)
                    numeros_detectados = pd.to_numeric(muestra_limpia, errors='coerce')
                    
                    if numeros_detectados.notna().mean() > 0.8:
                        st.session_state.num_cols.append(col)
                        st.session_state.cat_cols.remove(col)
                        # Limpiamos toda la columna en el DataFrame real
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,€£\s]', '', regex=True), errors='coerce')
                        
                st.success("¡Archivo cargado y variables identificadas automáticamente!")
            else:
                st.error("Hubo un error al leer el archivo. Asegúrate de que sea un CSV o Excel válido.")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin:18px 0 10px 0;">
          <div style="width:4px;height:20px;background:linear-gradient(180deg,#5ec4c8,#6366f1);border-radius:2px;"></div>
          <span style="font-size:14px;font-weight:700;color:#093134;letter-spacing:-.01em;">Vista previa de tus datos</span>
          <span style="font-size:11px;color:#6b9ea0;background:#f0fafa;border:1px solid #c8e8e9;padding:2px 9px;border-radius:999px;font-weight:500;">primeras 5 filas</span>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head())
        
        if not st.session_state.date_cols:
            st.warning("**No detectamos ninguna columna con Fechas.** Si tu archivo tiene fechas, por favor ve a 'Reclasificación de Variables' abajo y selecciónala manualmente. Las fechas son necesarias para predecir las ventas del día siguiente.", icon=":material/warning:")
            
        with st.expander("Reclasificación de Variables (Opcional)", expanded=False, icon=":material/tune:"):
            st.info("Hemos detectado automáticamente los tipos de datos de tus columnas. Puedes ajustarlos aquí si notas algún error (por ejemplo, si un código postal se detectó como numérico pero debería ser categórico).")
            col_d, col_n, col_c = st.columns(3)
            
            # Obtener todas las columnas del dataframe para el selector
            all_cols = df.columns.tolist()
            
            with col_d:
                date_cols = st.multiselect(":material/calendar_month: Fechas", all_cols, default=st.session_state.date_cols, key="m_date")
            with col_n:
                num_cols = st.multiselect(":material/payments: Numéricas", all_cols, default=st.session_state.num_cols, key="m_num")
            with col_c:
                cat_cols = st.multiselect(":material/label: Categóricas", all_cols, default=st.session_state.cat_cols, key="m_cat")
                
            st.session_state.date_cols = date_cols
            st.session_state.num_cols = num_cols
        analyses_to_remove = []
        global_insights_data = None
        
        for idx, analysis_config in enumerate(st.session_state.analyses):
            cid = analysis_config["id"]
            
            st.divider()
            
            col_h1, col_h2 = st.columns([8, 2])
            with col_h1:
                st.markdown(f'<h2 style="color:#093134;font-size:20px;font-weight:800;margin-top:30px;display:flex;align-items:center;gap:10px;"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#5ec4c8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg> Análisis {idx + 1}</h2>', unsafe_allow_html=True)
            with col_h2:
                if idx > 0:
                    if st.button("Eliminar Análisis", key=f"del_ana_{cid}", icon=":material/delete:"):
                        analyses_to_remove.append(idx)
            
            st.markdown('<div style="font-size:14px;font-weight:700;color:#093134;margin:15px 0 10px 0;display:flex;align-items:center;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#093134" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg> Configuración de Columnas</div>', unsafe_allow_html=True)
            if idx == 0:
                st.markdown("Configura las variables para este análisis. **Nota:** Esta primera configuración se usará también en el **Modelo de Predicción**.")
            
            date_opts = ["Ninguna"] + st.session_state.date_cols
            target_opts = ["Ninguna"] + st.session_state.num_cols
            cat_opts = ["Ninguna"] + st.session_state.cat_cols
            
            date_idx = date_opts.index(analysis_config["date_col"]) if analysis_config["date_col"] in date_opts else 0
            target_idx = target_opts.index(analysis_config["target_col"]) if analysis_config["target_col"] in target_opts else 0
            cat_idx = cat_opts.index(analysis_config["cat_col"]) if analysis_config["cat_col"] in cat_opts else 0
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                date_col = st.selectbox(":material/calendar_month: Columna de Fecha (Opcional)", date_opts, index=date_idx, key=f"date_{cid}")
            with col_b:
                target_col = st.selectbox(":material/payments: Variable Numérica (Eje Y)", target_opts, index=target_idx, key=f"target_{cid}")
            with col_c:
                cat_col = st.selectbox(":material/label: Variable Categórica (Eje X)", cat_opts, index=cat_idx, key=f"cat_{cid}")
            
            # Guardar configuración en tiempo real
            st.session_state.analyses[idx] = {
                "id": cid,
                "date_col": date_col if date_col != "Ninguna" else None,
                "target_col": target_col if target_col != "Ninguna" else None,
                "cat_col": cat_col if cat_col != "Ninguna" else None
            }
            
            config = st.session_state.analyses[idx]
            
            if config["target_col"] is not None:
                st.markdown(f'<h3 style="color:#093134;font-size:18px;font-weight:800;margin:35px 0 15px 0;display:flex;align-items:center;gap:10px;"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#5ec4c8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg> Métricas y Visualizaciones</h3>', unsafe_allow_html=True)
                
                target = config["target_col"]
                cat = config["cat_col"]
                date = config["date_col"]
                
                df_clean = df.copy()
                df_clean[target] = pd.to_numeric(df_clean[target], errors='coerce')
                df_clean = df_clean.dropna(subset=[target])
                
                if not df_clean.empty:
                    # Helpers para sparklines y KPIs (se usan más abajo en la línea de tiempo)
                    def make_sparkline_echarts(data, color, chart_type="line", is_area=False, spark_key="sp"):
                        series_obj = {
                            "data": data,
                            "type": chart_type,
                            "smooth": True,
                            "symbol": "none",
                            "itemStyle": {"color": color},
                            "lineStyle": {"color": color, "width": 2},
                        }
                        if is_area:
                            series_obj["areaStyle"] = {
                                "color": {
                                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                                    "colorStops": [
                                        {"offset": 0, "color": color + "4D"},
                                        {"offset": 1, "color": color + "00"},
                                    ]
                                }
                            }
                        if chart_type == "bar":
                            series_obj["itemStyle"] = {"color": color, "borderRadius": [3, 3, 0, 0]}
                        return {
                            "grid": {"top": 0, "bottom": 0, "left": 0, "right": 0},
                            "xAxis": {"type": "category", "show": False},
                            "yAxis": {"type": "value", "show": False, "min": "dataMin", "max": "dataMax"},
                            "series": [series_obj],
                            "animation": False,
                        }
    
                    def delta_html(delta_val):
                        if delta_val > 0:
                            return f'<span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:999px;font-size:13px;font-weight:600;">↑ +{delta_val:.1f}%</span>'
                        elif delta_val < 0:
                            return f'<span style="background:#fee2e2;color:#dc2626;padding:2px 8px;border-radius:999px;font-size:13px;font-weight:600;">↓ {delta_val:.1f}%</span>'
                        else:
                            return f'<span style="background:#f3f4f6;color:#6b7280;padding:2px 8px;border-radius:999px;font-size:13px;font-weight:600;">— 0.0%</span>'
    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # --- KPIs Categorías (Movidos aquí) ---
                    if cat is not None:
                        qty_cols = [c for c in df_clean.columns if ('cant' in c.lower() or 'qty' in c.lower() or 'unit' in c.lower()) and 'precio' not in c.lower() and 'price' not in c.lower() and 'unitario' not in c.lower()]
                        qty_col = qty_cols[0] if qty_cols else None
                        
                        st.markdown("<div class='sl-section-label'>Categorías y Producto</div>", unsafe_allow_html=True)
                        c1, c2, c3 = st.columns(3)
                        
                        cat_lider = "N/D"
                        cat_lider_pct_txt = "N/D"
                        tot_clean = df_clean[target].sum()
                        if not df_clean.empty and tot_clean > 0:
                            cat_group = df_clean.groupby(cat)[target].sum()
                            if not cat_group.empty:
                                cat_lider = str(cat_group.idxmax())
                                cat_lider_pct = (cat_group.max() / tot_clean) * 100
                                cat_lider_pct_txt = f"{cat_lider_pct:.1f}% del total"
                                
                        items_distintos = df_clean[cat].nunique()
                        
                        unidades_vendidas = "N/D"
                        unidades_txt = "Sin datos de cantidad"
                        if qty_col and pd.api.types.is_numeric_dtype(df_clean[qty_col]):
                            unidades_vendidas = f"{df_clean[qty_col].sum():,.0f}"
                            unidades_txt = "Productos Vendidos"
                            
                        # SVGs definition for Category KPIs
                        def svg_bg(color):
                            return f'<circle cx="36" cy="36" r="32" fill="{color}15"/>'
                        
                        svg_cat = f"""
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                          {svg_bg("#BA7517")}
                          <path d="M22 44 L26 26 L36 34 L46 26 L50 44 Z" fill="#BA7517" opacity="0.9">
                            <animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0" dur="2s" repeatCount="indefinite"/>
                          </path>
                          <circle cx="26" cy="23" r="2" fill="#fbbf24"/>
                          <circle cx="36" cy="31" r="2" fill="#fbbf24"/>
                          <circle cx="46" cy="23" r="2" fill="#fbbf24"/>
                          <line x1="24" y1="48" x2="48" y2="48" stroke="#BA7517" stroke-width="3" stroke-linecap="round"/>
                        </svg>"""

                        svg_item = f"""
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                          {svg_bg("#BA7517")}
                          <g>
                            <animateTransform attributeName="transform" type="translate" values="0,0;0,-2;0,0" dur="1.5s" repeatCount="indefinite"/>
                            <polygon points="36,24 22,30 36,36 50,30" fill="#BA7517" opacity="0.6"/>
                            <polygon points="22,30 36,36 36,50 22,44" fill="#BA7517" opacity="0.8"/>
                            <polygon points="50,30 36,36 36,50 50,44" fill="#BA7517" opacity="1"/>
                            <line x1="36" y1="36" x2="36" y2="50" stroke="#fff" stroke-width="1.5"/>
                            <line x1="22" y1="30" x2="36" y2="36" stroke="#fff" stroke-width="1.5"/>
                            <line x1="50" y1="30" x2="36" y2="36" stroke="#fff" stroke-width="1.5"/>
                          </g>
                        </svg>"""

                        svg_qty = f"""
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                          {svg_bg("#BA7517")}
                          <path d="M22 24 L26 24 L30 40 L48 40 L52 28 L28 28" fill="none" stroke="#BA7517" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                          <circle cx="32" cy="46" r="3" fill="#BA7517"><animateTransform attributeName="transform" type="rotate" values="0 32 46;360 32 46" dur="1s" repeatCount="indefinite"/></circle>
                          <circle cx="44" cy="46" r="3" fill="#BA7517"><animateTransform attributeName="transform" type="rotate" values="0 44 46;360 44 46" dur="1s" repeatCount="indefinite"/></circle>
                        </svg>"""

                        c1.markdown(make_card("Categoría Líder", cat_lider, cat_lider_pct_txt, svg_cat, delta=None), unsafe_allow_html=True)
                        c2.markdown(make_card("Ítems Distintos", f"{items_distintos:,}", f"Valores únicos", svg_item, delta=None), unsafe_allow_html=True)
                        c3.markdown(make_card("Unidades Vendidas", unidades_vendidas, unidades_txt, svg_qty, delta=None), unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                    # Gráficos
                    col_graf1, col_graf2 = st.columns(2)
                    
                    with col_graf1:
                        if cat is not None:
                            st.markdown(f"**Top por {cat}**")
                            df_cat = df_clean.groupby(cat)[target].sum().reset_index().sort_values(by=target, ascending=False).head(10)
                            
                            # Paleta de colores original de Plotly
                            plotly_colors = [
                                "#636efa", "#ef553b", "#00cc96", "#ab63fa", "#ffa15a",
                                "#19d3f3", "#ff6692", "#b6e880", "#ff97ff", "#fecb52"
                            ]
                            bar_categories = df_cat[cat].astype(str).tolist()
                            bar_values = df_cat[target].tolist()
                            bar_colors = [plotly_colors[i % len(plotly_colors)] for i in range(len(bar_categories))]
                            
                            bar_data = [
                                {"value": round(v, 2), "itemStyle": {"color": c}}
                                for v, c in zip(bar_values, bar_colors)
                            ]
                            
                            bar_options = {
                                "tooltip": {
                                    "trigger": "axis",
                                    "axisPointer": {"type": "shadow"},
                                },
                                "toolbox": {
                                    "feature": {
                                        "dataView": {"show": True, "readOnly": False},
                                        "magicType": {"show": True, "type": ["bar"]},
                                        "restore": {"show": True},
                                        "saveAsImage": {"show": True},
                                    }
                                },
                                "xAxis": [
                                    {
                                        "type": "category",
                                        "data": bar_categories,
                                        "axisPointer": {"type": "shadow"},
                                        "axisLabel": {"rotate": 30, "overflow": "truncate", "width": 80},
                                    }
                                ],
                                "yAxis": [
                                    {
                                        "type": "value",
                                        "name": target,
                                        "axisLabel": {"formatter": "{value}"},
                                        "splitLine": {"lineStyle": {"color": "rgba(128,128,128,0.2)"}},
                                    }
                                ],
                                "series": [
                                    {
                                        "name": target,
                                        "type": "bar",
                                        "data": bar_data,
                                        "label": {
                                            "show": True,
                                            "position": "top",
                                            "formatter": JsCode(
                                                "function(p){ var v=p.value; if(v>=1e6) return (v/1e6).toFixed(1)+'M'; if(v>=1e3) return (v/1e3).toFixed(1)+'K'; return v.toFixed(0); }"
                                            ).js_code,
                                        },
                                        "tooltip": {
                                            "valueFormatter": JsCode(
                                                "function(value){ return value.toLocaleString('es-CO', {minimumFractionDigits:2, maximumFractionDigits:2}); }"
                                            ).js_code
                                        },
                                    }
                                ],
                            }
                            st_echarts(options=bar_options, height="400px", key=f"bar_{cid}")
                        else:
                            st.info("Configura una 'Variable Categórica' para ver gráficas comparativas.")
                            
                    with col_graf2:
                        if cat is not None:
                            st.markdown(f"**Distribución de {target}**")
                            df_pie = df_clean.groupby(cat)[target].sum().reset_index().sort_values(by=target, ascending=False)
                            if len(df_pie) > 7:
                                top_6 = df_pie.head(6)
                                otros = pd.DataFrame({cat: ['Otros'], target: [df_pie.iloc[6:][target].sum()]})
                                df_pie = pd.concat([top_6, otros], ignore_index=True)
    
                            pie_data = [
                                {"value": round(row[target], 2), "name": str(row[cat])}
                                for _, row in df_pie.iterrows()
                            ]
    
                            pie_options = {
                                "tooltip": {
                                    "trigger": "item",
                                    "formatter": JsCode(
                                        "function(p){ return p.name + '<br/>' + p.percent.toFixed(1) + '%'; }"
                                    ).js_code,
                                },
                                "legend": {"top": "5%", "left": "center"},
                                "series": [
                                    {
                                        "name": target,
                                        "type": "pie",
                                        "radius": ["30%", "55%"],
                                        "center": ["50%", "60%"],
                                        "avoidLabelOverlap": True,
                                        "itemStyle": {
                                            "borderRadius": 10,
                                            "borderColor": "#fff",
                                            "borderWidth": 2,
                                        },
                                        "label": {
                                            "show": True,
                                            "formatter": JsCode(
                                                "function(p){ return p.name + '\\n' + p.percent.toFixed(1) + '%'; }"
                                            ).js_code,
                                            "fontSize": 12,
                                        },
                                        "emphasis": {
                                            "label": {
                                                "show": True,
                                                "fontSize": 18,
                                                "fontWeight": "bold",
                                                "formatter": JsCode(
                                                    "function(p){ return p.name + '\\n' + p.percent.toFixed(1) + '%'; }"
                                                ).js_code,
                                            }
                                        },
                                        "labelLine": {"show": True},
                                        "data": pie_data,
                                    }
                                ],
                            }
                            st_echarts(options=pie_options, height="400px", key=f"pie_{cid}")
                            
                    if date is not None:
                        st.markdown(f"**Evolución a lo largo del tiempo**")
                        df_clean[date] = pd.to_datetime(df_clean[date], errors='coerce')
                        df_time = df_clean.dropna(subset=[date])
                        
                        if not df_time.empty:
                            # Filtro por mes
                            df_time['MonthYear'] = df_time[date].dt.to_period('M')
                            available_months = sorted(df_time['MonthYear'].unique())
                            month_opts = ["Todos"] + [str(m) for m in available_months]
                            
                            selected_month = st.selectbox(
                                "Filtrar por Mes:", 
                                options=month_opts, 
                                index=0, 
                                key=f"month_filter_{cid}"
                            )
    
                            # ── KPI cards: solo en el primer análisis (idx == 0) ──
                            if idx == 0:
                                # Determinar el DataFrame del mes seleccionado y del anterior
                                if selected_month == "Todos":
                                    df_mes_actual = df_time.copy()
                                    df_mes_ant    = pd.DataFrame()   # sin comparativa
                                    label_mes     = "Total histórico"
                                else:
                                    periodo_actual = pd.Period(selected_month, freq='M')
                                    periodo_ant    = periodo_actual - 1
                                    df_mes_actual  = df_time[df_time['MonthYear'] == periodo_actual]
                                    df_mes_ant     = df_time[df_time['MonthYear'] == periodo_ant]
                                    label_mes      = selected_month

                                if df_mes_actual.empty:
                                    st.info("No hay datos para el período seleccionado.")
                                else:
                                    # --- Preparar Agrupaciones Diarias ---
                                    ventas_diarias_act = df_mes_actual.groupby(df_mes_actual[date].dt.date)[target].sum() if not df_mes_actual.empty else pd.Series(dtype=float)
                                    ventas_diarias_ant = df_mes_ant.groupby(df_mes_ant[date].dt.date)[target].sum() if not df_mes_ant.empty else pd.Series(dtype=float)

                                    # --- Cálculos Bloque 1 ---
                                    tot_act = df_mes_actual[target].sum()
                                    tot_ant = df_mes_ant[target].sum() if not df_mes_ant.empty else 0
                                    
                                    prom_act = df_mes_actual[target].mean()
                                    prom_ant = df_mes_ant[target].mean() if not df_mes_ant.empty else 0
                                    
                                    # Venta máxima del día
                                    max_dia_act = ventas_diarias_act.max() if not ventas_diarias_act.empty else 0
                                    max_dia_ant = ventas_diarias_ant.max() if not ventas_diarias_ant.empty else 0
                                    
                                    reg_act = len(df_mes_actual)
                                    reg_ant = len(df_mes_ant) if not df_mes_ant.empty else 0
                                    
                                    d_tot = safe_pct(tot_act, tot_ant)
                                    d_prom = safe_pct(prom_act, prom_ant)
                                    d_max = safe_pct(max_dia_act, max_dia_ant)
                                    d_reg = safe_pct(reg_act, reg_ant)
                                    
                                    # --- Cálculos Bloque 2 ---
                                    dias_con_ventas_act = len(ventas_diarias_act)
                                    dias_con_ventas_ant = len(ventas_diarias_ant)
                                    
                                    venta_diaria_prom_act = tot_act / dias_con_ventas_act if dias_con_ventas_act > 0 else 0
                                    venta_diaria_prom_ant = tot_ant / dias_con_ventas_ant if dias_con_ventas_ant > 0 else 0
                                    
                                    venta_min_diaria_act = ventas_diarias_act.min() if dias_con_ventas_act > 0 else 0
                                    venta_min_diaria_ant = ventas_diarias_ant.min() if dias_con_ventas_ant > 0 else 0
                                    
                                    d_vd_prom = safe_pct(venta_diaria_prom_act, venta_diaria_prom_ant)
                                    d_dias = safe_pct(dias_con_ventas_act, dias_con_ventas_ant)
                                    d_vmin = safe_pct(venta_min_diaria_act, venta_min_diaria_ant)
                                    
                                    # Tendencia reciente
                                    ultimos_7 = ventas_diarias_act.sort_index().tail(7)
                                    tendencia_color = "#6b7280"
                                    tendencia_custom_border = "#B4B2A9"
                                    if len(ultimos_7) > 1:
                                        x = np.arange(len(ultimos_7))
                                        y = ultimos_7.values
                                        slope, _ = np.polyfit(x, y, 1)
                                        umbral = 0.01 * (y.mean() if y.mean() != 0 else 1)
                                        if slope > umbral:
                                            tendencia_txt = '<span style="color:#16a34a;font-weight:600;">Creciente ↑</span>'
                                            tendencia_color = "#16a34a"
                                            tendencia_custom_border = "#1D9E75"
                                        elif slope < -umbral:
                                            tendencia_txt = '<span style="color:#dc2626;font-weight:600;">Decreciente ↓</span>'
                                            tendencia_color = "#dc2626"
                                            tendencia_custom_border = "#E24B4A"
                                        else:
                                            tendencia_txt = '<span style="color:#6b7280;font-weight:600;">Estable →</span>'
                                    else:
                                        tendencia_txt = '<span style="color:#6b7280;font-weight:600;">N/D</span>'

                                    # SVGs
                                    def svg_bg(color):
                                        return f'<circle cx="36" cy="36" r="32" fill="{color}15"/>'
                                        
                                    svg_total = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_tot))}
                                      <ellipse cx="36" cy="45" rx="16" ry="14" fill="{icon_color(d_tot)}" opacity="0.85"/>
                                      <rect x="30" y="28" width="12" height="8" rx="3" fill="{icon_color(d_tot)}" opacity="0.7"/>
                                      <ellipse cx="36" cy="28" rx="6" ry="3" fill="{icon_color(d_tot)}" opacity="0.5"/>
                                      <text x="36" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="white" font-family="sans-serif">$</text>
                                      <circle cx="52" cy="18" r="5" fill="#fbbf24" opacity="0.9"><animate attributeName="cy" values="18;12;18" dur="1.4s" repeatCount="indefinite"/></circle>
                                      <circle cx="20" cy="14" r="3" fill="#fbbf24" opacity="0.7"><animate attributeName="cy" values="14;8;14" dur="1.8s" repeatCount="indefinite"/></circle>
                                    </svg>"""

                                    svg_prom = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_prom))}
                                      <rect x="34.5" y="24" width="3" height="26" rx="1.5" fill="{icon_color(d_prom)}" opacity="0.8"/>
                                      <ellipse cx="36" cy="50" rx="9" ry="2.5" fill="{icon_color(d_prom)}" opacity="0.5"/>
                                      <g transform-origin="36 30">
                                        <animateTransform attributeName="transform" type="rotate" values="0 36 30;-8 36 30;0 36 30;8 36 30;0 36 30" dur="3s" repeatCount="indefinite"/>
                                        <rect x="16" y="28.5" width="40" height="3" rx="1.5" fill="{icon_color(d_prom)}" opacity="0.9"/>
                                        <line x1="20" y1="31" x2="16" y2="41" stroke="{icon_color(d_prom)}" stroke-width="1.5"/>
                                        <ellipse cx="16" cy="42" rx="6" ry="2" fill="{icon_color(d_prom)}" opacity="0.7"/>
                                        <line x1="52" y1="31" x2="56" y2="41" stroke="{icon_color(d_prom)}" stroke-width="1.5"/>
                                        <ellipse cx="56" cy="42" rx="6" ry="2" fill="{icon_color(d_prom)}" opacity="0.7"/>
                                      </g>
                                      <circle cx="36" cy="24" r="3" fill="{icon_color(d_prom)}"/>
                                    </svg>"""

                                    svg_max = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_max))}
                                      <ellipse cx="36" cy="56" rx="5" ry="8" fill="#f97316" opacity="0.8"><animate attributeName="ry" values="8;12;8;10;8" dur="0.6s" repeatCount="indefinite"/></ellipse>
                                      <g><animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0" dur="1.2s" repeatCount="indefinite"/>
                                        <ellipse cx="36" cy="32" rx="8" ry="14" fill="{icon_color(d_max)}"/>
                                        <polygon points="36,14 30,26 42,26" fill="{icon_color(d_max)}"/>
                                        <circle cx="36" cy="32" r="3" fill="#fff" opacity="0.9"/>
                                        <polygon points="28,43 23,52 30,47" fill="{icon_color(d_max)}" opacity="0.8"/>
                                        <polygon points="44,43 49,52 42,47" fill="{icon_color(d_max)}" opacity="0.8"/>
                                      </g>
                                    </svg>"""

                                    svg_reg = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_reg))}
                                      <circle cx="36" cy="24" r="7" fill="{icon_color(d_reg)}" opacity="0.9"/>
                                      <path d="M22 49 Q22 36 36 36 Q50 36 50 49" fill="{icon_color(d_reg)}" opacity="0.9"/>
                                      <circle cx="18" cy="28" r="5" fill="{icon_color(d_reg)}" opacity="0.55"/>
                                      <path d="M8 49 Q8 38 18 38 Q25 38 27 45" fill="{icon_color(d_reg)}" opacity="0.45"/>
                                      <circle cx="54" cy="28" r="5" fill="{icon_color(d_reg)}" opacity="0.55"/>
                                      <path d="M64 49 Q64 38 54 38 Q47 38 45 45" fill="{icon_color(d_reg)}" opacity="0.45"/>
                                    </svg>"""

                                    svg_vd_prom = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_vd_prom))}
                                      <rect x="20" y="24" width="32" height="28" rx="4" fill="none" stroke="{icon_color(d_vd_prom)}" stroke-width="2.5"/>
                                      <line x1="26" y1="20" x2="26" y2="26" stroke="{icon_color(d_vd_prom)}" stroke-width="2.5" stroke-linecap="round"/>
                                      <line x1="46" y1="20" x2="46" y2="26" stroke="{icon_color(d_vd_prom)}" stroke-width="2.5" stroke-linecap="round"/>
                                      <line x1="20" y1="32" x2="52" y2="32" stroke="{icon_color(d_vd_prom)}" stroke-width="2.5"/>
                                      <circle cx="36" cy="42" r="6" fill="none" stroke="{icon_color(d_vd_prom)}" stroke-width="2"/>
                                      <line x1="36" y1="42" x2="36" y2="38" stroke="{icon_color(d_vd_prom)}" stroke-width="2"><animateTransform attributeName="transform" type="rotate" values="0 36 42;360 36 42" dur="2s" repeatCount="indefinite"/></line>
                                    </svg>"""

                                    svg_dias = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_dias))}
                                      <rect x="22" y="22" width="28" height="28" rx="3" fill="{icon_color(d_dias)}" opacity="0.2"/>
                                      <rect x="26" y="18" width="28" height="28" rx="3" fill="none" stroke="{icon_color(d_dias)}" stroke-width="2.5" fill-opacity="0"/>
                                      <path d="M34 32 L39 37 L46 27" fill="none" stroke="{icon_color(d_dias)}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                        <animate attributeName="stroke-dasharray" values="0,30;30,0" dur="1.5s" repeatCount="indefinite"/>
                                      </path>
                                    </svg>"""

                                    svg_vmin = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(icon_color(d_vmin))}
                                      <path d="M36 46 L26 28 L46 28 Z" fill="{icon_color(d_vmin)}" opacity="0.8">
                                        <animateTransform attributeName="transform" type="translate" values="0,-4;0,2;0,-4" dur="2s" repeatCount="indefinite"/>
                                      </path>
                                      <line x1="22" y1="52" x2="50" y2="52" stroke="{icon_color(d_vmin)}" stroke-width="3" stroke-linecap="round"/>
                                    </svg>"""

                                    svg_tend = f"""
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="56" height="56">
                                      {svg_bg(tendencia_color)}
                                      <polyline points="20,44 32,32 40,38 52,24" fill="none" stroke="{tendencia_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                        <animate attributeName="stroke-dasharray" values="0,60;60,0" dur="2s" repeatCount="indefinite"/>
                                      </polyline>
                                      <circle cx="52" cy="24" r="3" fill="{tendencia_color}"/>
                                    </svg>"""

                                    # --- UI Bloque 1 ---
                                    st.markdown(f"<div class='sl-section-label'>Ventas — {label_mes}</div>", unsafe_allow_html=True)
                                    c1, c2, c3, c4 = st.columns(4)
                                    c1.markdown(make_card("Total Ventas", f"{tot_act:,.2f}", format_delta(d_tot) + " vs anterior", svg_total, delta=d_tot), unsafe_allow_html=True)
                                    c2.markdown(make_card("Ticket Promedio", f"{prom_act:,.2f}" if pd.notna(prom_act) else "N/D", format_delta(d_prom) + " vs anterior", svg_prom, delta=d_prom), unsafe_allow_html=True)
                                    c3.markdown(make_card("Día de Venta Máxima", f"{max_dia_act:,.2f}" if pd.notna(max_dia_act) else "N/D", format_delta(d_max) + " vs anterior", svg_max, delta=d_max), unsafe_allow_html=True)
                                    c4.markdown(make_card("Total Registros", f"{reg_act:,}", format_delta(d_reg) + " vs anterior", svg_reg, delta=d_reg), unsafe_allow_html=True)
                                    
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    
                                    # --- UI Bloque 2 ---
                                    st.markdown("<div class='sl-section-label'>Rendimiento Operacional</div>", unsafe_allow_html=True)
                                    c1, c2, c3, c4 = st.columns(4)
                                    c1.markdown(make_card("Venta Diaria Promedio", f"{venta_diaria_prom_act:,.2f}", format_delta(d_vd_prom) + " vs anterior", svg_vd_prom, delta=d_vd_prom), unsafe_allow_html=True)
                                    c2.markdown(make_card("Días con Ventas", f"{dias_con_ventas_act}", format_delta(d_dias) + " vs anterior", svg_dias, delta=d_dias), unsafe_allow_html=True)
                                    c3.markdown(make_card("Día de Venta Mínima", f"{venta_min_diaria_act:,.2f}" if pd.notna(venta_min_diaria_act) else "N/D", format_delta(d_vmin) + " vs anterior", svg_vmin, delta=d_vmin), unsafe_allow_html=True)
                                    c4.markdown(make_card("Tendencia (Últ. 7d)", tendencia_txt, "Basado en reg. lineal", svg_tend, delta=None, custom_color=tendencia_custom_border), unsafe_allow_html=True)
                                    
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    
                                    st.markdown("<br>", unsafe_allow_html=True)
                            # ── fin KPI cards ──
                            
                            df_time_full = df_time.copy()
                            
                            if selected_month != "Todos":
                                df_time = df_time[df_time['MonthYear'].astype(str) == selected_month]
                                
                            # Agrupar por la fecha/hora exacta para soportar datos intradía o diarios
                            df_line = df_time.groupby(date)[target].sum().reset_index()
                            df_line = df_line.sort_values(by=date)
                            
                            series_data = []
                            for _, row in df_line.iterrows():
                                ts = int(row[date].timestamp() * 1000)
                                val = row[target]
                                series_data.append([ts, val])
                                
                            options = {
                                "useUTC": True,
                                "title": {
                                    "text": f"Evolución de {target} en el tiempo",
                                    "left": "center",
                                    "textStyle": {"fontSize": 16, "color": "#111827", "fontFamily": "sans-serif"}
                                },
                                "tooltip": {"show": True, "trigger": "axis"},
                                "xAxis": [
                                    {
                                        "type": "time",
                                        "axisLabel": {
                                            "showMinLabel": True,
                                            "showMaxLabel": True,
                                            "formatter": JsCode(
                                                '''
                                  (value, index, extra) => {
                                    if (!extra || !extra.break) {
                                      return echarts.time.format(value, '{yyyy}-{MM}-{dd} {HH}:{mm}', true);
                                    }
                                    if (extra.break.type === 'start') {
                                      return (
                                        echarts.time.format(extra.break.start, '{yyyy}-{MM}-{dd} {HH}:{mm}', true) +
                                        '/' +
                                        echarts.time.format(extra.break.end, '{yyyy}-{MM}-{dd} {HH}:{mm}', true)
                                      );
                                    }
                                    return '';
                                  }
                                '''
                                            ).js_code,
                                        },
                                        "breakLabelLayout": {"moveOverlap": False},
                                        "breaks": [],
                                        "breakArea": {
                                            "expandOnClick": False,
                                            "zigzagAmplitude": 0,
                                            "zigzagZ": 200,
                                        },
                                    }
                                ],
                                "yAxis": {"type": "value", "min": "dataMin"},
                                "dataZoom": [
                                    {"type": "inside", "xAxisIndex": 0},
                                    {"type": "slider", "xAxisIndex": 0},
                                ],
                                "series": [{
                                    "type": "line", 
                                    "symbolSize": 0, 
                                    "data": series_data,
                                    "itemStyle": {"color": "#093134"},
                                    "lineStyle": {"color": "#093134"}
                                }],
                            }
                            st_echarts(options=options, height="500px", key=f"line_{cid}")
                            
                            st.markdown('<br>', unsafe_allow_html=True)
                            
                            # --- HEATMAP ---
                            st.markdown("<div style='font-size:16px;font-weight:700;color:#111827;margin-bottom:10px;text-align:center;'>Ventas por día de la semana</div>", unsafe_allow_html=True)
                            hm_df = df_time.copy()
                            hm_df[date] = pd.to_datetime(hm_df[date])
                            hm_df['DiaSemana'] = hm_df[date].dt.dayofweek
                            hm_df['Semana_Lunes'] = hm_df[date] - pd.to_timedelta(hm_df['DiaSemana'], unit='d')
                            hm_df['Semana_Lunes'] = hm_df['Semana_Lunes'].dt.date
                            
                            hm_group = hm_df.groupby(['Semana_Lunes', 'DiaSemana'])[target].sum().reset_index()
                            
                            semanas = sorted(hm_group['Semana_Lunes'].unique())
                            semanas_str = [str(s) for s in semanas]
                            semanas_dict = {s: i for i, s in enumerate(semanas)}
                            
                            hm_data = []
                            for _, row in hm_group.iterrows():
                                x_idx = semanas_dict[row['Semana_Lunes']]
                                y_idx = 6 - int(row['DiaSemana'])
                                val = round(row[target], 2)
                                hm_data.append([x_idx, y_idx, val])
                                
                            heatmap_options = {
                                "backgroundColor": "transparent",
                                "tooltip": {
                                    "position": "top",
                                    "formatter": JsCode('''
                                        function (params) {
                                            var weeks = ''' + str(semanas_str) + ''';
                                            var days = ["Domingo", "Sábado", "Viernes", "Jueves", "Miércoles", "Martes", "Lunes"];
                                            var date = weeks[params.value[0]];
                                            var day = days[params.value[1]];
                                            var valStr = (params.value[2] !== undefined && params.value[2] !== null) ? params.value[2].toLocaleString('en-US', {maximumFractionDigits: 2}) : '0';
                                            return date + ' (' + day + '): <b>' + valStr + '</b>';
                                        }
                                    ''').js_code
                                },
                                "grid": {"height": "70%", "top": "10%", "right": "5%", "left": "10%"},
                                "xAxis": {
                                    "type": "category",
                                    "data": semanas_str,
                                    "splitArea": {"show": True}
                                },
                                "yAxis": {
                                    "type": "category",
                                    "data": ["Domingo", "Sábado", "Viernes", "Jueves", "Miércoles", "Martes", "Lunes"],
                                    "splitArea": {"show": True}
                                },
                                "visualMap": {
                                    "min": 0,
                                    "max": float(hm_group[target].max()) if not hm_group.empty else 100,
                                    "calculable": True,
                                    "orient": "horizontal",
                                    "left": "center",
                                    "bottom": "0%",
                                    "inRange": {
                                        "color": ["#f3f4f6", "#085041"]
                                    }
                                },
                                "series": [{
                                    "name": "Ventas",
                                    "type": "heatmap",
                                    "data": hm_data,
                                    "label": {"show": False},
                                    "itemStyle": {
                                        "borderColor": "#fff",
                                        "borderWidth": 1
                                    }
                                }]
                            }
                            st_echarts(options=heatmap_options, height="400px", key=f"heatmap_{cid}")
                            
                            st.markdown('<br>', unsafe_allow_html=True)
                            
                            # --- Resumen Inteligente (Insights Engine) ---
                            if idx == 0 and not df_mes_actual.empty:
                                global_insights_data = {
                                    'tot_act': tot_act,
                                    'tot_ant': tot_ant,
                                    'd_tot': d_tot,
                                    'prom_act': prom_act,
                                    'prom_ant': prom_ant,
                                    'd_prom': d_prom,
                                    'ventas_diarias_act': ventas_diarias_act,
                                    'df_mes_actual': df_mes_actual,
                                    'date_col': date,
                                    'target_col': target,
                                    'cat_lider': cat_lider if 'cat_lider' in locals() else None,
                                    'cat_lider_pct': cat_lider_pct if 'cat_lider_pct' in locals() else 0
                                }
                            
                else:
                    st.warning("No hay datos numéricos válidos en la columna seleccionada.")
            else:
                st.warning("Selecciona una 'Variable Numérica (Eje Y)' para generar los gráficos de este análisis.", icon=":material/warning:")
                
        if analyses_to_remove:
            for i in sorted(analyses_to_remove, reverse=True):
                st.session_state.analyses.pop(i)
            st.rerun()
    
        st.divider()
        if st.button("Añadir nuevo análisis", use_container_width=True, icon=":material/add:"):
            st.session_state.analyses.append({
                "id": st.session_state.analysis_counter, 
                "date_col": None, 
                "target_col": None, 
                "cat_col": None
            })
            st.session_state.analysis_counter += 1
            st.rerun()
            
        if global_insights_data is not None:
            render_insights_section(global_insights_data)
    
