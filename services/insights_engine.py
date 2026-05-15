import streamlit as st
import pandas as pd
import numpy as np

def generate_sales_insights(tot_act, tot_ant, d_tot):
    if d_tot is None:
        return {"tipo": "info", "icono": "📊", "color": "#3b82f6", "bg": "#eff6ff", "border": "#bfdbfe", 
                "texto": f"Durante el período analizado, se registraron ventas totales por <b>${tot_act:,.0f}</b>."}
    
    if d_tot > 0:
        return {"tipo": "positivo", "icono": "🚀", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                "texto": f"Las ventas crecieron un <b>{d_tot:.1f}%</b> respecto al mes anterior, alcanzando <b>${tot_act:,.0f}</b>."}
    elif d_tot < 0:
        return {"tipo": "alerta", "icono": "📉", "color": "#dc2626", "bg": "#fef2f2", "border": "#fecaca",
                "texto": f"Las ventas presentan una caída del <b>{abs(d_tot):.1f}%</b> este mes. Considera activar promociones."}
    else:
        return {"tipo": "info", "icono": "➖", "color": "#6b7280", "bg": "#f9fafb", "border": "#e5e7eb",
                "texto": "Las ventas se mantuvieron sin cambios respecto al periodo anterior."}

def generate_ticket_insights(prom_act, prom_ant, d_prom):
    if d_prom is None or pd.isna(prom_act):
        return None
    if d_prom > 0:
        return {"tipo": "positivo", "icono": "🛍️", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                "texto": f"La venta promedio por día aumentó a <b>${prom_act:,.0f}</b> (+{d_prom:.1f}%), indicando compras de mayor valor por cliente."}
    elif d_prom < 0:
        return {"tipo": "atencion", "icono": "⚠️", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a",
                "texto": f"La venta promedio por día disminuyó un <b>{abs(d_prom):.1f}%</b>. Sugerimos implementar estrategias de venta cruzada."}
    return None

def generate_trend_insights(ventas_diarias_act):
    ultimos_7 = ventas_diarias_act.sort_index().tail(7)
    if len(ultimos_7) > 1:
        x = np.arange(len(ultimos_7))
        y = ultimos_7.values
        slope, _ = np.polyfit(x, y, 1)
        umbral = 0.01 * (y.mean() if y.mean() != 0 else 1)
        
        if slope > umbral:
            return {"tipo": "positivo", "icono": "📈", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                    "texto": "La tendencia de los últimos 7 días muestra crecimiento constante en el flujo comercial."}
        elif slope < -umbral:
            return {"tipo": "alerta", "icono": "⚠️", "color": "#dc2626", "bg": "#fef2f2", "border": "#fecaca",
                    "texto": "Las ventas muestran tendencia a la baja en la última semana. Recomendamos revisar el stock o el tráfico de clientes."}
        else:
            return {"tipo": "info", "icono": "⚖️", "color": "#3b82f6", "bg": "#eff6ff", "border": "#bfdbfe",
                    "texto": "El comportamiento comercial reciente se mantiene estable y sin fluctuaciones graves."}
    return None

def generate_day_insights(df_mes_actual, date_col, target_col):
    df = df_mes_actual.copy()
    # Paso 1: sumar todas las ventas de cada día calendario
    df['_fecha_solo'] = df[date_col].dt.date
    df['DiaSemana'] = df[date_col].dt.dayofweek
    suma_diaria = df.groupby(['_fecha_solo', 'DiaSemana'])[target_col].sum().reset_index()
    # Paso 2: promediar esas sumas diarias por día de la semana (lunes=0 … domingo=6)
    promedio_por_dia = suma_diaria.groupby('DiaSemana')[target_col].mean()
    
    if promedio_por_dia.empty:
        return None
        
    dias_es = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    
    dia_fuerte = promedio_por_dia.idxmax()
    dia_debil = promedio_por_dia.idxmin()
    
    max_val = promedio_por_dia.max()
    min_val = promedio_por_dia.min()
    
    insights = []
    if max_val > 0 and (max_val / (min_val if min_val > 0 else 1)) > 1.3:
        insights.append({"tipo": "positivo", "icono": "⭐", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                "texto": f"Los <b>{dias_es[dia_fuerte]}s</b> son los días con mejor rendimiento promedio en ventas de este mes."})
        insights.append({"tipo": "atencion", "icono": "💡", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a",
                "texto": f"Los <b>{dias_es[dia_debil]}s</b> presentan menor actividad comercial. Se recomienda lanzar ofertas especiales esos días."})
    return insights

def generate_category_insights(cat_lider, cat_lider_pct):
    if cat_lider and cat_lider != "N/D" and cat_lider_pct > 0:
        if cat_lider_pct > 50:
            return {"tipo": "atencion", "icono": "🎯", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a",
                    "texto": f"Existe alta dependencia comercial: la categoría <b>'{cat_lider}'</b> concentra el <b>{cat_lider_pct:.1f}%</b> de todos los ingresos."}
        else:
            return {"tipo": "positivo", "icono": "🏆", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                    "texto": f"La categoría <b>'{cat_lider}'</b> lidera tus ingresos, aportando saludablemente el <b>{cat_lider_pct:.1f}%</b> del total."}
    return None

def generate_stability_insights(ventas_diarias_act):
    if len(ventas_diarias_act) > 3:
        cv = ventas_diarias_act.std() / (ventas_diarias_act.mean() if ventas_diarias_act.mean() != 0 else 1)
        if cv < 0.3:
            return {"tipo": "positivo", "icono": "🌊", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0",
                    "texto": "El negocio mantiene un flujo de ventas muy predecible y consistente día tras día."}
        elif cv > 0.8:
            return {"tipo": "atencion", "icono": "📊", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a",
                    "texto": "Se detectan variaciones e inestabilidad notables entre los días de operación. Asegúrate de tener cobertura adecuada."}
    return None

def render_insights_section(datos_insights):
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('''
        <div style="margin-top: 20px; margin-bottom: 25px;">
            <h2 style="color: #093134; font-size: 24px; font-weight: 800; display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#5ec4c8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
                Resumen Inteligente del Negocio
            </h2>
            <p style="color: #4a6e70; font-size: 15px; margin-top: 0; font-weight: 500;">Interpretación automática de los principales indicadores, hallazgos y oportunidades detectadas en este período.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    insights = []
    
    if 'd_tot' in datos_insights:
        insights.append(generate_sales_insights(datos_insights['tot_act'], datos_insights['tot_ant'], datos_insights['d_tot']))
        
    if 'd_prom' in datos_insights:
        insights.append(generate_ticket_insights(datos_insights['prom_act'], datos_insights['prom_ant'], datos_insights['d_prom']))
    
    if 'ventas_diarias_act' in datos_insights:
        insights.append(generate_trend_insights(datos_insights['ventas_diarias_act']))
        insights.append(generate_stability_insights(datos_insights['ventas_diarias_act']))
        
    if 'df_mes_actual' in datos_insights and 'date_col' in datos_insights and 'target_col' in datos_insights:
        dias_ins = generate_day_insights(datos_insights['df_mes_actual'], datos_insights['date_col'], datos_insights['target_col'])
        if dias_ins:
            insights.extend(dias_ins)
            
    if 'cat_lider' in datos_insights and 'cat_lider_pct' in datos_insights:
        insights.append(generate_category_insights(datos_insights['cat_lider'], datos_insights['cat_lider_pct']))
        
    insights = [i for i in insights if i is not None]
    
    if not insights:
        st.info("No hay suficientes datos para generar insights inteligentes en este período.")
        return
        
    for i in range(0, len(insights), 2):
        col1, col2 = st.columns(2)
        ins1 = insights[i]
        
        html1 = f"""
        <div class="sl-insight-card" style="background-color: {ins1['bg']}; border-left: 5px solid {ins1['color']}; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); display: flex; gap: 16px; align-items: flex-start; height: 100%;">
            <div class="sl-insight-icon" style="font-size: 26px; line-height: 1; flex-shrink: 0;">{ins1['icono']}</div>
            <div style="color: #1f2937; font-size: 15px; line-height: 1.6;">
                {ins1['texto']}
            </div>
        </div>
        """
        col1.markdown(html1, unsafe_allow_html=True)
        
        if i + 1 < len(insights):
            ins2 = insights[i+1]
            html2 = f"""
            <div class="sl-insight-card" style="background-color: {ins2['bg']}; border-left: 5px solid {ins2['color']}; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); display: flex; gap: 16px; align-items: flex-start; height: 100%;">
                <div class="sl-insight-icon" style="font-size: 26px; line-height: 1; flex-shrink: 0;">{ins2['icono']}</div>
                <div style="color: #1f2937; font-size: 15px; line-height: 1.6;">
                    {ins2['texto']}
                </div>
            </div>
            """
            col2.markdown(html2, unsafe_allow_html=True)
        else:
            col2.empty()
