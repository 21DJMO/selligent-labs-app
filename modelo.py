import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

def mostrar_modelo():
    # ── Mini Hero para la página de Modelo ──
    st.markdown("""<div style="background:linear-gradient(135deg,#093134 0%,#0e5558 100%);border-radius:15px;padding:36px;margin-bottom:30px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.15);"><div style="position:absolute;top:-20px;right:-20px;width:120px;height:120px;border-radius:50%;background:rgba(94,196,200,0.1);"></div><div style="position:relative;z-index:1;"><div style="color:#ffffff; font-size:28px; font-weight:800; letter-spacing:-0.02em; line-height:1.2;">Predicción Inteligente</div><div style="color:#b0d8da; font-size:15px; font-weight:500; margin-top:8px;">Nuestra Inteligencia Artificial proyecta tu desempeño para los próximos 7 días</div></div></div>""", unsafe_allow_html=True)
    
    df = st.session_state.df
    config = st.session_state.analyses[0]
    
    if df is None:
        st.warning("Primero ve a la pestaña de 'Análisis de Ventas' y carga tu archivo de datos.")
    elif config["target_col"] is None or config["date_col"] is None:
        st.warning("⚠️ Para usar la predicción, necesitas configurar la **Variable Numérica** y la **Columna de Fecha** en el primer bloque de Análisis de Ventas.")
    else:
        target = config["target_col"]
        date = config["date_col"]
        
        df_temp = df.copy()
        df_temp[date] = pd.to_datetime(df_temp[date], errors='coerce')
        df_temp[target] = pd.to_numeric(df_temp[target], errors='coerce')
        df_temp = df_temp.dropna(subset=[date, target])
        
        # Agrupar por día
        df_time = df_temp.groupby(df_temp[date].dt.date)[target].sum().reset_index()
        df_time = df_time.sort_values(by=date)
        df_time.rename(columns={date: 'ds', target: 'y'}, inplace=True)
        df_time['ds'] = pd.to_datetime(df_time['ds'])
        
        # Limitar a los últimos 90 días para entrenamiento y visualización
        df_time = df_time.tail(90).copy()
        
        if len(df_time) < 15:
            st.error("Se requieren al menos 15 días de historial para generar predicciones con Inteligencia Artificial.")
            return
            
        with st.spinner("Analizando patrones y entrenando Inteligencia Artificial..."):
            # 1. Feature Engineering
            df_ml = df_time.copy()
            df_ml['dayofweek'] = df_ml['ds'].dt.dayofweek
            df_ml['lag_1'] = df_ml['y'].shift(1)
            df_ml['lag_2'] = df_ml['y'].shift(2)
            df_ml['lag_3'] = df_ml['y'].shift(3)
            df_ml['lag_7'] = df_ml['y'].shift(7)
            df_ml['rolling_mean_7'] = df_ml['y'].shift(1).rolling(window=7).mean()
            
            df_ml = df_ml.dropna()
            
            if len(df_ml) < 7:
                st.error("No hay suficientes datos históricos. Por favor carga un archivo con un rango de fechas más amplio.")
                return

            X_train = df_ml[['dayofweek', 'lag_1', 'lag_2', 'lag_3', 'lag_7', 'rolling_mean_7']]
            y_train = df_ml['y']
            
            # 2. Modelo Random Forest
            rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
            rf.fit(X_train, y_train)
            
            # 3. Calcular % de Confianza basado en el Error Absoluto Porcentual (MAPE)
            y_pred_train = rf.predict(X_train)
            mape = mean_absolute_percentage_error(y_train, y_pred_train)
            confianza = max(0, min(100, (1 - mape) * 100))
            
            # 4. Predicción a 7 días
            historial_y = df_time['y'].values.tolist()
            ultimo_dia = df_time['ds'].iloc[-1]
            
            fechas_futuras = [ultimo_dia + pd.Timedelta(days=i) for i in range(1, 8)]
            predicciones = []
            
            for i in range(7):
                dow = fechas_futuras[i].dayofweek
                l1 = historial_y[-1]
                l2 = historial_y[-2]
                l3 = historial_y[-3]
                l7 = historial_y[-7] if len(historial_y) >= 7 else np.mean(historial_y[-7:])
                rm7 = np.mean(historial_y[-7:]) if len(historial_y) >= 7 else np.mean(historial_y)
                
                feat = pd.DataFrame({
                    'dayofweek': [dow],
                    'lag_1': [l1],
                    'lag_2': [l2],
                    'lag_3': [l3],
                    'lag_7': [l7],
                    'rolling_mean_7': [rm7]
                })
                
                pred = rf.predict(feat)[0]
                predicciones.append(max(0, pred))
                historial_y.append(max(0, pred))
                
            total_predicho = sum(predicciones)
            
        # ==========================================
        # INTERFAZ DE USUARIO (MÉTRICAS Y GRÁFICAS)
        # ==========================================
        st.markdown("<h2 style='color:#093134;font-weight:800;font-size:22px;margin-bottom:16px;'>Resumen de Proyección</h2>", unsafe_allow_html=True)
        
        # KPIs con SVG cards estilizadas
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="
                border:1.5px solid #d0e8e9;
                border-radius:14px;
                padding:22px 24px;
                background:#f5fafa;
                height:100%;
            ">
                <div style="display:flex; align-items:center; gap: 12px; margin-bottom:12px;">
                    <div style="font-size:28px;">💰</div>
                    <div style="font-weight:700;color:#4a6e70;font-size:14px;text-transform:uppercase;letter-spacing:0.05em;">Ingresos Proyectados (7 días)</div>
                </div>
                <div style="color:#093134;font-size:36px;font-weight:800;letter-spacing:-0.02em;margin-bottom:8px;">${total_predicho:,.2f}</div>
                <div style="display:inline-block;background:#dcfce7;color:#16a34a;font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;">
                    ✨ Inteligencia Artificial Activada
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="
                border:1.5px solid #d0e8e9;
                border-radius:14px;
                padding:22px 24px;
                background:#f5fafa;
                height:100%;
            ">
                <div style="display:flex; align-items:center; gap: 12px; margin-bottom:12px;">
                    <div style="font-size:28px;">🎯</div>
                    <div style="font-weight:700;color:#4a6e70;font-size:14px;text-transform:uppercase;letter-spacing:0.05em;">Nivel de Confianza de la IA</div>
                </div>
                <div style="color:#093134;font-size:36px;font-weight:800;letter-spacing:-0.02em;margin-bottom:8px;">{confianza:.1f}%</div>
                <div style="color:#4a6e70;font-size:13px;font-weight:500;">
                    Basado en el aprendizaje de tu historial reciente
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráfica Echarts
        df_plot_hist = df_time.copy()
        
        series_hist = []
        for _, row in df_plot_hist.iterrows():
            ts = int(row['ds'].timestamp() * 1000)
            series_hist.append([ts, row['y']])
            
        series_pred = []
        # Conectar la línea de predicción con el último punto del histórico
        ultimo_ts = int(df_plot_hist['ds'].iloc[-1].timestamp() * 1000)
        ultimo_y = df_plot_hist['y'].iloc[-1]
        series_pred.append([ultimo_ts, ultimo_y])
        
        for dt, val in zip(fechas_futuras, predicciones):
            ts = int(dt.timestamp() * 1000)
            series_pred.append([ts, val])
            
        options = {
            "useUTC": True,
            "title": {
                "text": "Evolución y Proyección a 7 Días",
                "left": "center",
            },
            "tooltip": {
                "show": True, 
                "trigger": "axis",
                "valueFormatter": JsCode("function(value){ return value.toLocaleString('es-CO', {style: 'currency', currency: 'COP'}); }").js_code
            },
            "legend": {"data": ["Ventas Históricas", "Proyección"], "bottom": 0},
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
                  return echarts.time.format(value, '{yyyy}-{MM}-{dd}', true);
                }
                return '';
              }
            """
                        ).js_code,
                    },
                }
            ],
            "yAxis": {"type": "value", "min": "dataMin"},
            "dataZoom": [
                {"type": "inside", "xAxisIndex": 0},
                {"type": "slider", "xAxisIndex": 0},
            ],
            "series": [
                {
                    "name": "Ventas Históricas",
                    "type": "line", 
                    "symbolSize": 0, 
                    "data": series_hist,
                    "itemStyle": {"color": "#093134"},
                    "lineStyle": {"color": "#093134", "width": 2}
                },
                {
                    "name": "Proyección",
                    "type": "line", 
                    "symbolSize": 6,
                    "itemStyle": {"color": "#16a34a"},
                    "lineStyle": {"color": "#16a34a", "type": "dashed", "width": 3},
                    "data": series_pred
                }
            ],
        }
        st_echarts(options=options, height="500px", key="line_pred_echart")
        
        # Explicación "Friendly" para el usuario final
        st.markdown("""
        <div style="
            border:1.5px solid #d0e8e9;
            border-radius:16px;
            padding:20px 24px;
            background:#f5fafa;
            display:flex;
            align-items:flex-start;
            gap:16px;
            margin-top:16px;
        ">
            <div style="font-size:32px;flex-shrink:0;">💡</div>
            <div>
                <div style="font-size:15px;font-weight:800;color:#093134;margin-bottom:4px;">¿Cómo funciona esta predicción?</div>
                <p style="color:#4a6e70;font-size:14px;line-height:1.6;margin:0;">
                    El sistema analiza factores como los días de la semana en los que más vendes, tus promedios móviles recientes y ciclos pasados. 
                    No es magia, es <strong>matemática adaptada a las particularidades de tu negocio</strong>.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)