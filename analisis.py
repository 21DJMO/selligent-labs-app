import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode

@st.cache_data
def load_data(file):
        if file.name.endswith('.csv'):
            try:
                file.seek(0)
                df = pd.read_csv(file)
                # Si pandas lee todo como una sola columna y tiene punto y coma, el separador era ';'
                if len(df.columns) == 1 and ';' in df.columns[0]:
                    file.seek(0)
                    df = pd.read_csv(file, sep=';', encoding='utf-8')
                    if len(df.columns) == 1: # Si sigue fallando con utf-8 probamos latin1
                        file.seek(0)
                        df = pd.read_csv(file, sep=';', encoding='latin1')
                return df
            except:
                file.seek(0)
                return pd.read_csv(file, sep=';', encoding='latin1')
        elif file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file)
        return None
    
    
def mostrar_analisis():
    # ── Mini Hero para la página de Análisis ──
    st.markdown("""<div style="background:linear-gradient(135deg,#093134 0%,#0e5558 100%);border-radius:15px;padding:36px;margin-bottom:30px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.15);"><div style="position:absolute;top:-20px;right:-20px;width:120px;height:120px;border-radius:50%;background:rgba(94,196,200,0.1);"></div><div style="position:relative;z-index:1;"><div style="color:#ffffff; font-size:28px; font-weight:800; letter-spacing:-0.02em; line-height:1.2;">Análisis de Ventas</div><div style="color:#b0d8da; font-size:15px; font-weight:500; margin-top:8px;">Transforma tus registros en decisiones estratégicas</div></div></div>""", unsafe_allow_html=True)
    
    st.markdown('<h2 style="color:#093134;font-size:20px;font-weight:800;margin-bottom:15px;display:flex;align-items:center;gap:10px;"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#5ec4c8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Carga de Datos</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#f0fafa;border-left:4px solid #5ec4c8;padding:16px 20px;border-radius:0 10px 10px 0;margin-bottom:20px;">
        <div style="font-size:14px;font-weight:700;color:#093134;margin-bottom:5px;display:flex;align-items:center;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px;"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .34 2.02 1.5 3.5.76.76 1.23 1.52 1.41 2.5"></path></svg> ¿Cómo obtengo mis datos?</div>
        <div style="font-size:13.5px;color:#4a6e70;line-height:1.5;">
            La mayoría de los sistemas (POS, Shopify, facturación) permiten exportar ventas diarias. 
            Busca la opción <b>"Exportar a Excel"</b> o <b>"CSV"</b>.
        </div>
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
        st.markdown("**Vista previa de tus datos:**")
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
            st.session_state.cat_cols = cat_cols
        
        analyses_to_remove = []
        
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
                                        "radius": ["40%", "70%"],
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
    
                                def mes_delta(col, df_act, df_ant):
                                    if df_ant.empty:
                                        return 0.0
                                    v_act = df_act[col].sum()
                                    v_ant = df_ant[col].sum()
                                    if v_ant == 0:
                                        return 0.0
                                    return ((v_act - v_ant) / abs(v_ant)) * 100
    
                                total_mes   = df_mes_actual[target].sum()
                                prom_mes    = df_mes_actual[target].mean()
                                max_mes     = df_mes_actual[target].max()
                                reg_mes     = len(df_mes_actual)
    
                                d_total = mes_delta(target, df_mes_actual, df_mes_ant)
                                d_prom  = mes_delta(target, df_mes_actual, df_mes_ant)
                                d_max   = 0.0
                                d_reg   = 0.0
                                if not df_mes_ant.empty:
                                    r_ant = len(df_mes_ant)
                                    d_reg = ((reg_mes - r_ant) / abs(r_ant)) * 100 if r_ant else 0.0
    
                                # Sparkline del mes actual
                                df_spark_mes = df_mes_actual.groupby(date)[target].sum().reset_index().sort_values(date)
                                spark_vals = df_spark_mes[target].tolist()
                                if len(spark_vals) > 30:
                                    step = len(spark_vals) // 30
                                    spark_vals = spark_vals[::step][:30]
                                spark_rounded = [round(v, 2) for v in spark_vals] if spark_vals else [0]
    
                                hint = "" if selected_month == "Todos" else " vs mes anterior"
                                st.markdown(f"**Resumen de Métricas Principales** — {label_mes}{hint}")
    
                                # Color del icono según delta (verde/rojo/gris)
                                def icon_color(delta):
                                    if delta > 0: return "#16a34a"
                                    elif delta < 0: return "#dc2626"
                                    else: return "#6b7280"
    
                                # SVG: bolsa de dinero con monedas animadas cayendo — Total
                                svg_total = f"""
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="72" height="72">
                                  <defs>
                                    <radialGradient id="bg1_{cid}" cx="50%" cy="50%" r="50%">
                                      <stop offset="0%" stop-color="{icon_color(d_total)}22"/>
                                      <stop offset="100%" stop-color="{icon_color(d_total)}08"/>
                                    </radialGradient>
                                  </defs>
                                  <circle cx="40" cy="40" r="36" fill="url(#bg1_{cid})"/>
                                  <!-- bolsa -->
                                  <ellipse cx="40" cy="50" rx="18" ry="16" fill="{icon_color(d_total)}" opacity="0.85"/>
                                  <ellipse cx="40" cy="50" rx="18" ry="16" fill="none" stroke="{icon_color(d_total)}" stroke-width="1.5"/>
                                  <rect x="33" y="32" width="14" height="8" rx="4" fill="{icon_color(d_total)}" opacity="0.7"/>
                                  <ellipse cx="40" cy="32" rx="7" ry="4" fill="{icon_color(d_total)}" opacity="0.5"/>
                                  <!-- signo $ -->
                                  <text x="40" y="55" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="sans-serif">$</text>
                                  <!-- moneda animada -->
                                  <circle cx="58" cy="20" r="6" fill="#fbbf24" opacity="0.9">
                                    <animate attributeName="cy" values="20;14;20" dur="1.4s" repeatCount="indefinite"/>
                                    <animate attributeName="opacity" values="0.9;0.4;0.9" dur="1.4s" repeatCount="indefinite"/>
                                  </circle>
                                  <circle cx="22" cy="16" r="4" fill="#fbbf24" opacity="0.7">
                                    <animate attributeName="cy" values="16;10;16" dur="1.8s" repeatCount="indefinite"/>
                                    <animate attributeName="opacity" values="0.7;0.2;0.7" dur="1.8s" repeatCount="indefinite"/>
                                  </circle>
                                </svg>"""
    
                                # SVG: balanza de equilibrio animada — Promedio (color neutro fijo)
                                svg_prom = f"""
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="72" height="72">
                                  <defs>
                                    <radialGradient id="bg2_{cid}" cx="50%" cy="50%" r="50%">
                                      <stop offset="0%" stop-color="#6b728022"/>
                                      <stop offset="100%" stop-color="#6b728008"/>
                                    </radialGradient>
                                  </defs>
                                  <circle cx="40" cy="40" r="36" fill="url(#bg2_{cid})"/>
                                  <!-- poste -->
                                  <rect x="38.5" y="28" width="3" height="28" rx="1.5" fill="#6b7280" opacity="0.8"/>
                                  <ellipse cx="40" cy="56" rx="10" ry="3" fill="#6b7280" opacity="0.5"/>
                                  <!-- barra horizontal con balanceo -->
                                  <g transform-origin="40 34">
                                    <animateTransform attributeName="transform" type="rotate" values="0 40 34;-8 40 34;0 40 34;8 40 34;0 40 34" dur="3s" repeatCount="indefinite"/>
                                    <rect x="18" y="32.5" width="44" height="3" rx="1.5" fill="#6b7280" opacity="0.9"/>
                                    <!-- platillo izquierdo -->
                                    <line x1="22" y1="35" x2="18" y2="46" stroke="#6b7280" stroke-width="1.5"/>
                                    <ellipse cx="18" cy="47" rx="7" ry="2.5" fill="#6b7280" opacity="0.7"/>
                                    <!-- platillo derecho -->
                                    <line x1="58" y1="35" x2="62" y2="46" stroke="#6b7280" stroke-width="1.5"/>
                                    <ellipse cx="62" cy="47" rx="7" ry="2.5" fill="#6b7280" opacity="0.7"/>
                                  </g>
                                  <!-- punto central -->
                                  <circle cx="40" cy="28" r="3.5" fill="#6b7280"/>
                                </svg>"""
    
                                # SVG: cohete despegando — Máximo
                                svg_max = f"""
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="72" height="72">
                                  <defs>
                                    <radialGradient id="bg3_{cid}" cx="50%" cy="50%" r="50%">
                                      <stop offset="0%" stop-color="#f59e0b22"/>
                                      <stop offset="100%" stop-color="#f59e0b08"/>
                                    </radialGradient>
                                  </defs>
                                  <circle cx="40" cy="40" r="36" fill="url(#bg3_{cid})"/>
                                  <!-- llama animada -->
                                  <ellipse cx="40" cy="62" rx="6" ry="9" fill="#f97316" opacity="0.8">
                                    <animate attributeName="ry" values="9;13;9;11;9" dur="0.6s" repeatCount="indefinite"/>
                                    <animate attributeName="opacity" values="0.8;1;0.6;1;0.8" dur="0.6s" repeatCount="indefinite"/>
                                  </ellipse>
                                  <ellipse cx="40" cy="62" rx="3.5" ry="6" fill="#fde68a">
                                    <animate attributeName="ry" values="6;9;6;8;6" dur="0.6s" repeatCount="indefinite"/>
                                  </ellipse>
                                  <!-- cohete cuerpo -->
                                  <g>
                                    <animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0" dur="1.2s" repeatCount="indefinite"/>
                                    <ellipse cx="40" cy="36" rx="9" ry="16" fill="#6366f1"/>
                                    <!-- punta -->
                                    <polygon points="40,16 33,30 47,30" fill="#4f46e5"/>
                                    <!-- ventana -->
                                    <circle cx="40" cy="36" r="4" fill="#bae6fd" opacity="0.9"/>
                                    <!-- aletas -->
                                    <polygon points="31,48 26,58 33,52" fill="#4f46e5" opacity="0.8"/>
                                    <polygon points="49,48 54,58 47,52" fill="#4f46e5" opacity="0.8"/>
                                  </g>
                                  <!-- estrellas -->
                                  <circle cx="18" cy="22" r="1.5" fill="#fbbf24"><animate attributeName="opacity" values="1;0;1" dur="1.5s" repeatCount="indefinite"/></circle>
                                  <circle cx="62" cy="18" r="1" fill="#fbbf24"><animate attributeName="opacity" values="0;1;0" dur="1.2s" repeatCount="indefinite"/></circle>
                                  <circle cx="55" cy="32" r="1.5" fill="#fbbf24"><animate attributeName="opacity" values="1;0;1" dur="2s" repeatCount="indefinite"/></circle>
                                </svg>"""
    
                                # SVG: personas/usuarios con pulso — Registros
                                svg_reg = f"""
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="72" height="72">
                                  <defs>
                                    <radialGradient id="bg4_{cid}" cx="50%" cy="50%" r="50%">
                                      <stop offset="0%" stop-color="{icon_color(d_reg)}22"/>
                                      <stop offset="100%" stop-color="{icon_color(d_reg)}08"/>
                                    </radialGradient>
                                  </defs>
                                  <circle cx="40" cy="40" r="36" fill="url(#bg4_{cid})"/>
                                  <!-- persona central -->
                                  <circle cx="40" cy="26" r="8" fill="{icon_color(d_reg)}" opacity="0.9"/>
                                  <path d="M24 54 Q24 40 40 40 Q56 40 56 54" fill="{icon_color(d_reg)}" opacity="0.9"/>
                                  <!-- persona izquierda -->
                                  <circle cx="20" cy="30" r="6" fill="{icon_color(d_reg)}" opacity="0.55"/>
                                  <path d="M8 54 Q8 42 20 42 Q28 42 30 50" fill="{icon_color(d_reg)}" opacity="0.45"/>
                                  <!-- persona derecha -->
                                  <circle cx="60" cy="30" r="6" fill="{icon_color(d_reg)}" opacity="0.55"/>
                                  <path d="M72 54 Q72 42 60 42 Q52 42 50 50" fill="{icon_color(d_reg)}" opacity="0.45"/>
                                  <!-- pulso animado -->
                                  <circle cx="40" cy="26" r="10" fill="none" stroke="{icon_color(d_reg)}" stroke-width="1.5" opacity="0">
                                    <animate attributeName="r" values="10;20;10" dur="2s" repeatCount="indefinite"/>
                                    <animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/>
                                  </circle>
                                </svg>"""
    
                                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
                                with kpi1:
                                    st.markdown(f"""
                                    <div style="border:1px solid #e5e7eb;border-radius:16px;padding:20px 22px 18px 22px;background:#fff;display:flex;align-items:center;justify-content:space-between;min-height:110px;">
                                        <div>
                                            <div style="color:#6b7280;font-size:13px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;">Total de {target}</div>
                                            <div style="font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;line-height:1;">{total_mes:,.2f}</div>
                                            {delta_html(d_total)}
                                        </div>
                                        <div style="flex-shrink:0;margin-left:12px;">{svg_total}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
    
                                with kpi2:
                                    st.markdown(f"""
                                    <div style="border:1px solid #e5e7eb;border-radius:16px;padding:20px 22px 18px 22px;background:#fff;display:flex;align-items:center;justify-content:space-between;min-height:110px;">
                                        <div>
                                            <div style="color:#6b7280;font-size:13px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;">Promedio de {target}</div>
                                            <div style="font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;line-height:1;">{prom_mes:,.2f}</div>
                                        </div>
                                        <div style="flex-shrink:0;margin-left:12px;">{svg_prom}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
    
                                with kpi3:
                                    st.markdown(f"""
                                    <div style="border:1px solid #e5e7eb;border-radius:16px;padding:20px 22px 18px 22px;background:#fff;display:flex;align-items:center;justify-content:space-between;min-height:110px;">
                                        <div>
                                            <div style="color:#6b7280;font-size:13px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;">Máximo de {target}</div>
                                            <div style="font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;line-height:1;">{max_mes:,.2f}</div>
                                        </div>
                                        <div style="flex-shrink:0;margin-left:12px;">{svg_max}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
    
                                with kpi4:
                                    st.markdown(f"""
                                    <div style="border:1px solid #e5e7eb;border-radius:16px;padding:20px 22px 18px 22px;background:#fff;display:flex;align-items:center;justify-content:space-between;min-height:110px;">
                                        <div>
                                            <div style="color:#6b7280;font-size:13px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;">Registros</div>
                                            <div style="font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;line-height:1;">{reg_mes:,}</div>
                                            {delta_html(d_reg)}
                                        </div>
                                        <div style="flex-shrink:0;margin-left:12px;">{svg_reg}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
    
                                st.markdown("<br>", unsafe_allow_html=True)
                            # ── fin KPI cards ──
                            
                            if selected_month != "Todos":
                                df_time = df_time[df_time['MonthYear'].astype(str) == selected_month]
                                
                            # Agrupar por la fecha/hora exacta para soportar datos intradía o diarios
                            df_time = df_time.groupby(date)[target].sum().reset_index()
                            df_time = df_time.sort_values(by=date)
                            
                            series_data = []
                            for _, row in df_time.iterrows():
                                ts = int(row[date].timestamp() * 1000)
                                val = row[target]
                                series_data.append([ts, val])
                                
                            options = {
                                "useUTC": True,
                                "title": {
                                    "text": f"Evolución de {target} en el tiempo",
                                    "left": "center",
                                },
                                "tooltip": {"show": True, "trigger": "axis"},
                                "xAxis": [
                                    {
                                        "type": "time",
                                        "axisLabel": {
                                            "showMinLabel": True,
                                            "showMaxLabel": True,
                                            "formatter": JsCode(
                                                """
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
                                """
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
    
