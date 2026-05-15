def make_card(label, value, subtext, svg_icon, delta=None, custom_color=None):
    border_color = "#B4B2A9"
    if custom_color is not None:
        border_color = custom_color
    elif delta is not None:
        if delta > 0: border_color = "#1D9E75"
        elif delta < 0: border_color = "#E24B4A"
        
    tooltip_text = ""
    if label == "Total Ventas": tooltip_text = "Ingresos totales del período seleccionado, antes de descontar costos o gastos."
    elif label == "Venta Promedio": tooltip_text = "Valor promedio por transacción registrada. Incrementarlo es una de las formas más eficientes de crecer sin aumentar el volumen de clientes."
    elif label == "Día de Venta Máx.": tooltip_text = "Mayor ingreso registrado en un solo día del período. Identifica qué lo generó para poder replicarlo."
    elif label == "Total Registros": tooltip_text = "Número de transacciones registradas en el período. Un valor inusualmente bajo puede indicar que el archivo subido está incompleto."
    elif label == "Venta Diaria Prom.": tooltip_text = "Promedio de ingresos por día operativo. Útil para proyectar el cierre del mes y detectar días atípicos."
    elif label == "Días con Ventas": tooltip_text = "Días del período con al menos una transacción registrada. Permite identificar días sin actividad o con datos faltantes."
    elif label == "Día de venta min.": tooltip_text = "Menor ingreso registrado en un día del período. Valores muy bajos pueden corresponder a festivos, cierres o registros incompletos."
    elif label == "Tendencia (Últ. 7d)": tooltip_text = "Dirección de las ventas en los últimos 7 días, calculada por regresión lineal. Indica si el negocio va al alza, a la baja o se mantiene estable."
    elif label == "Categoría Líder": tooltip_text = "El producto o categoría que más ingresos generó. Asegúrate de que nunca le falte stock."
    elif label == "Ítems Distintos": tooltip_text = "Cuántos productos o categorías diferentes vendiste. Alta variedad puede diluir el foco."
    elif label == "Unidades vendidas": tooltip_text = "Total de unidades o cantidad vendida según tu columna de cantidad."

    tooltip_html = f'<span title="{tooltip_text}" style="cursor:help;margin-left:4px;color:#9ca3af;font-size:12px;">ⓘ</span>'

    # CSS variable --kpi-border lets the CSS :hover rule animate border-left-width
    # without fighting inline-style specificity
    return f"""
    <div class="sl-kpi-card" style="--kpi-border:{border_color};">
        <div style="flex:1;min-width:0;">
            <div style="color:#6b7280;font-size:11px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;font-weight:600;display:flex;align-items:center;">{label}{tooltip_html}</div>
            <div class="sl-kpi-value" style="font-size:22px;font-weight:800;color:#111827;margin-bottom:6px;line-height:1;word-break:break-word;">{value}</div>
            <div style="font-size:12px;color:#4b5563;">{subtext}</div>
        </div>
        <div class="sl-kpi-icon" style="flex-shrink:0;margin-left:16px;">{svg_icon}</div>
    </div>
    """
