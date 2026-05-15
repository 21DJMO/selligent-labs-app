"""
modelo.py — Página "Predicción Inteligente" de Selligent Labs
Random Forest simplificado · 8 features temporales · sin variables categóricas
Walk-Forward Validation · GridSearchCV compacto · Forecasting recursivo a 7d
"""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
from services.predict_engine import train_model, FORECAST_DAYS, WINDOW_DAYS

# ─────────────────────────────────────────
#  PÁGINA PRINCIPAL
# ─────────────────────────────────────────
def mostrar_modelo():
    # ── Hero header
    st.markdown("""
    <style>
    @keyframes _mgrad { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
    @keyframes _morb  { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-16px) scale(1.06)} }
    @keyframes _mdot  { 0%,100%{opacity:.2;transform:scale(1)} 50%{opacity:.9;transform:scale(1.3)} }
    @keyframes _mchip { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    </style>
    <div style="background:linear-gradient(135deg,#041e20 0%,#062527 25%,#093134 55%,#0e5558 80%,#145055 100%);background-size:400% 400%;animation:_mgrad 10s ease-in-out infinite;border-radius:22px;padding:48px 52px 42px;margin-bottom:36px;position:relative;overflow:hidden;border:1px solid rgba(94,196,200,0.25);box-shadow:0 24px 60px rgba(0,0,0,0.35),0 0 0 1px rgba(94,196,200,0.08) inset;">
      <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(94,196,200,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(94,196,200,0.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;"></div>
      <div style="position:absolute;top:-80px;right:-80px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(94,196,200,0.18) 0%,transparent 65%);animation:_morb 7s ease-in-out infinite;"></div>
      <div style="position:absolute;bottom:-90px;right:140px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(5,150,105,0.14) 0%,transparent 65%);animation:_morb 9s ease-in-out infinite reverse;"></div>
      <div style="position:absolute;top:30px;left:-50px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,0.10) 0%,transparent 65%);animation:_morb 11s ease-in-out infinite;"></div>
      <div style="position:absolute;top:32px;right:260px;width:6px;height:6px;border-radius:50%;background:#5ec4c8;animation:_mdot 2.4s ease-in-out infinite;"></div>
      <div style="position:absolute;top:58px;right:295px;width:4px;height:4px;border-radius:50%;background:#34d399;animation:_mdot 3.1s ease-in-out infinite 0.5s;"></div>
      <div style="position:absolute;bottom:44px;left:210px;width:5px;height:5px;border-radius:50%;background:#a5b4fc;animation:_mdot 2.7s ease-in-out infinite 1s;"></div>
      <div style="position:absolute;bottom:0;left:52px;right:52px;height:2px;background:linear-gradient(90deg,transparent,rgba(5,150,105,0.7) 30%,rgba(94,196,200,0.8) 70%,transparent);border-radius:2px;"></div>
      <div style="position:relative;z-index:1;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:22px;">
          <span class="sl-banner-badge" style="background:rgba(94,196,200,0.15);color:#7dd9dd;border-color:rgba(94,196,200,0.35);animation:_mchip .5s ease both;">&#129302; Inteligencia de Negocio</span>
          <span class="sl-banner-badge" style="background:rgba(5,150,105,0.12);color:#6ee7b7;border-color:rgba(5,150,105,0.3);animation:_mchip .5s .12s ease both;">&#9989; An&#225;lisis Verificado</span>
        </div>
        <div style="color:#fff;font-size:clamp(28px,3.8vw,42px);font-weight:900;letter-spacing:-.04em;line-height:1.1;margin-bottom:14px;">
          Predicci&#243;n <span style="color:#5ec4c8;text-shadow:0 0 28px rgba(94,196,200,0.5);">Inteligente</span>
        </div>
        <div style="color:#b0d4d6;font-size:15px;font-weight:400;line-height:1.7;max-width:560px;margin-bottom:24px;">Proyecta el comportamiento de tus ventas para los pr&#243;ximos d&#237;as bas&#225;ndose en el historial de tu negocio.</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
          <div class="sl-banner-chip" style="animation:_mchip .5s .2s ease both;">
            <span>&#128200;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">Tendencias futuras</span>
          </div>
          <div class="sl-banner-chip" style="animation:_mchip .5s .3s ease both;">
            <span>&#128197;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">Proyecci&#243;n pr&#243;ximos 7 d&#237;as</span>
          </div>
          <div class="sl-banner-chip" style="animation:_mchip .5s .4s ease both;">
            <span>&#9889;</span><span style="color:#e2f0f1;font-size:12px;font-weight:600;">An&#225;lisis autom&#225;tico</span>
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    df     = st.session_state.get('df')
    config = st.session_state.get('analyses', [{}])[0]

    if df is None:
        st.warning("Primero ve a **Análisis de Ventas** y carga tu archivo de datos.")
        return
    if not config.get('target_col') or not config.get('date_col'):
        st.warning("⚠️ Configura la **Variable Numérica** y la **Columna de Fecha** "
                   "en el bloque de Análisis de Ventas.")
        return

    target   = config['target_col']
    date_col = config['date_col']

    # Preprocesar: solo fecha y target, agrupado por día
    raw = df.dropna(subset=[date_col, target]).copy()
    raw[target]   = pd.to_numeric(raw[target], errors='coerce')
    raw[date_col] = pd.to_datetime(raw[date_col], errors='coerce')
    raw = raw.dropna(subset=[date_col, target])

    daily = (raw.groupby(raw[date_col].dt.date)[target]
               .sum().reset_index())
    daily.columns        = ['ds', 'y']
    daily['ds']          = pd.to_datetime(daily['ds'])
    
    # RELLENAR HUECOS: Asegurar que todos los días existan en la serie
    if not daily.empty:
        all_dates = pd.date_range(start=daily['ds'].min(), end=daily['ds'].max(), freq='D')
        daily = daily.set_index('ds').reindex(all_dates, fill_value=0).reset_index()
        daily.columns = ['ds', 'y']

    daily                = daily.sort_values('ds').reset_index(drop=True)

    if len(daily) < 15:
        st.error("Se necesitan al menos 15 días de historial.")
        return

    # ── Entrenamiento (cacheado) ─────────────────────────────
    with st.spinner("Analizando patrones y entrenando modelo…"):
        result = train_model(daily.to_json())

    if result is None:
        st.error("No hay suficientes datos después de construir las features.")
        return

    preds        = result['preds']
    future_dates = [pd.Timestamp(d) for d in result['future_dates']]
    confianza    = result['confianza']
    total_pred   = result['total_pred']
    mape_wf      = result['mape_wf']
    mape_std     = result['mape_std']
    feat_imp     = result['feat_imp']
    best_params  = result['best_params']

    # ── KPI Cards ────────────────────────────────────────────
    st.markdown("<h2 style='color:#093134;font-weight:800;font-size:22px;"
                "margin-bottom:16px;'>Resumen de Proyección</h2>",
                unsafe_allow_html=True)

    # No longer needed as we use .sl-kpi-card class

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="sl-kpi-card" style="--kpi-border:#5ec4c8;">
          <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
              <span style="font-weight:700;color:#4a6e70;font-size:13px;
                  text-transform:uppercase;letter-spacing:.05em;">
                Ingresos Proyectados (7d)
              </span>
            </div>
            <div class="sl-kpi-value" style="color:#093134;font-size:34px;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:8px;">${total_pred:,.2f}</div>
            <div style="display:inline-block;background:#dcfce7;color:#16a34a;
                font-size:12px;font-weight:600;padding:4px 10px;
                border-radius:999px;">✨ IA Activada</div>
          </div>
          <div class="sl-kpi-icon" style="font-size:32px;">💰</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        bc, tc = ("#dcfce7","#16a34a") if confianza >= 70 else \
                 ("#fef9c3","#b45309") if confianza >= 50 else \
                 ("#fee2e2","#dc2626")
        st.markdown(f"""
        <div class="sl-kpi-card" style="--kpi-border:{tc};">
          <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
              <span style="font-weight:700;color:#4a6e70;font-size:13px;
                  text-transform:uppercase;letter-spacing:.05em;">
                Nivel de Confianza
              </span>
            </div>
            <div class="sl-kpi-value" style="color:#093134;font-size:34px;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:8px;">{confianza:.1f}%</div>
            <div style="display:inline-block;background:{bc};color:{tc};
                font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;">
              MAPE walk-forward: {mape_wf:.1f}% ± {mape_std:.1f}%
            </div>
          </div>
          <div class="sl-kpi-icon" style="font-size:32px;">🎯</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        avg = total_pred / FORECAST_DAYS
        st.markdown(f"""
        <div class="sl-kpi-card" style="--kpi-border:#5ec4c8;">
          <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
              <span style="font-weight:700;color:#4a6e70;font-size:13px;
                  text-transform:uppercase;letter-spacing:.05em;">
                Promedio Diario
              </span>
            </div>
            <div class="sl-kpi-value" style="color:#093134;font-size:34px;font-weight:800;
                letter-spacing:-0.02em;margin-bottom:8px;">${avg:,.2f}</div>
            <div style="color:#4a6e70;font-size:13px;font-weight:500;">
              Basado en {len(daily)} días de historial
            </div>
          </div>
          <div class="sl-kpi-icon" style="font-size:32px;">📅</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráfica ECharts ──────────────────────────────────────
    show_n     = min(30, len(result['hist_dates']))
    hist_dates = result['hist_dates'][-show_n:]
    hist_y     = result['hist_y'][-show_n:]

    series_hist = [[d, round(v, 2)] for d, v in zip(hist_dates, hist_y)]
    series_pred = [[hist_dates[-1], round(hist_y[-1], 2)]]  # conectar
    for dt, val in zip(future_dates, preds):
        series_pred.append([dt.strftime('%Y-%m-%d'), round(val, 2)])

    options = {
        "title": {"text": "Evolución y Proyección a 7 Días", "left": "center"},
        "tooltip": {
            "trigger": "axis",
            "valueFormatter": JsCode(
                "function(v){ return '$'+v.toLocaleString('es-CO',"
                "{minimumFractionDigits:2}); }"
            ).js_code,
        },
        "legend": {"data": ["Ventas Históricas", "Proyección RF"], "bottom": 0},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value", "min": "dataMin"},
        "dataZoom": [
            {"type": "inside", "xAxisIndex": 0},
            {"type": "slider", "xAxisIndex": 0},
        ],
        "series": [
            {
                "name": "Ventas Históricas",
                "type": "line",
                "data": series_hist,
                "symbolSize": 0,
                "itemStyle":  {"color": "#093134"},
                "lineStyle":  {"color": "#093134", "width": 2},
                "areaStyle":  {"color": "#09313415"},
            },
            {
                "name": "Proyección RF",
                "type": "line",
                "data": series_pred,
                "symbolSize": 7,
                "itemStyle": {"color": "#059669"},
                "lineStyle": {"color": "#059669", "type": "dashed", "width": 3},
            },
        ],
    }
    st_echarts(options=options, height="500px", key="pred_echart_v3")

    # ── Tabla de predicciones ────────────────────────────────
    st.markdown("<h3 style='color:#093134;font-weight:700;font-size:18px;"
                "margin-top:24px;margin-bottom:12px;'>Detalle por Día</h3>",
                unsafe_allow_html=True)

    pred_df = pd.DataFrame({
        'Fecha':      [d.strftime('%a %d %b %Y') for d in future_dates],
        'Proyección': [f"${v:,.2f}" for v in preds],
    })
    st.dataframe(pred_df, use_container_width=True, hide_index=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Nota explicativa ─────────────────────────────────────
    st.markdown("""
    <div style="border:1.5px solid #d0e8e9;border-radius:16px;
        padding:20px 24px;background:#f5fafa;
        display:flex;align-items:flex-start;gap:16px;margin-top:16px;">
      <div style="font-size:32px;flex-shrink:0;">💡</div>
      <div>
        <div style="font-size:15px;font-weight:800;color:#093134;margin-bottom:4px;">
          ¿Cómo funciona esta predicción?
        </div>
        <p style="color:#4a6e70;font-size:14px;line-height:1.6;margin:0;">
          El modelo analiza <strong>patrones del día de la semana</strong>,
          <strong>ventas recientes</strong> (últimas 1, 2, 3 y 7 jornadas),
          y el <strong>promedio y variabilidad de la última semana</strong>.
          Este conjunto compacto de 8 variables maximiza la generalización
          con pocos datos. La <em>confianza</em> se mide con validación
          temporal real (Walk-Forward), no sobre datos de entrenamiento.
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)