import streamlit as st

def mostrar_inicio():
    # ── Hero Section ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#093134 0%,#0e5558 60%,#1a7a7f 100%);border-radius:20px;padding:52px 48px 44px 48px;margin-bottom:36px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-40px;right:-40px;width:220px;height:220px;border-radius:50%;background:rgba(94,196,200,0.08);"></div>
        <div style="position:absolute;bottom:-60px;right:80px;width:160px;height:160px;border-radius:50%;background:rgba(94,196,200,0.05);"></div>
        <div style="position:relative;z-index:1;">
            <span style="display:inline-block;background:rgba(94,196,200,0.18);color:#5ec4c8;font-size:12px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:5px 14px;border-radius:999px;border:1px solid #5ec4c840;margin-bottom:24px;">📊 Inteligencia de Negocio — Sin complicaciones</span>
            <div style="margin-bottom:12px;">
                <span style="font-size:clamp(38px,5vw,58px);font-weight:900;color:#ffffff;letter-spacing:-0.03em;line-height:1.05;">Selligent</span><span style="font-size:clamp(38px,5vw,58px);font-weight:900;color:#5ec4c8;letter-spacing:-0.03em;line-height:1.05;"> Labs</span>
            </div>
            <div style="color:#ffffff;font-size:clamp(18px,2.2vw,24px);font-weight:700;margin:0 0 14px 0;line-height:1.3;letter-spacing:-0.01em;">Inteligencia para tu negocio.</div>
            <div style="color:#e0f5f6;font-size:16px;line-height:1.8;max-width:600px;margin:0 0 12px 0;font-weight:400;">
                Sube tu archivo de ventas en segundos. Detectamos tus datos automáticamente,
                generamos visualizaciones interactivas y en el futuro
                predeciremos el comportamiento de tus ventas
                con Machine Learning. <span style="color:#5ec4c8;font-weight:600;">Sin código. Sin Power BI. Sin analista.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    
    # ── ¿Para quién es? ──
    st.markdown("""
    <h2 style="color:#093134;font-weight:800;font-size:22px;margin-bottom:6px;">¿Para quién es esta herramienta?</h2>
    <p style="color:#4a6e70;font-size:15px;margin-bottom:24px;">
        Diseñada específicamente para <strong>pequeños negocios</strong> que quieren tomar decisiones
        basadas en datos, sin pagar por un analista ni aprender a programar.
    </p>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    perfiles = [
        ("🛍️", "Tienda física o e-commerce", "Llevas tus ventas en Excel o las exportas de tu POS/Shopify. Quieres saber qué productos venden más y cómo evolucionan mes a mes."),
        ("🍽️", "Restaurante o negocio de comida", "Registras tus pedidos o facturación diaria. Quieres ver en qué días vendes más y cuáles productos son tu motor de ingresos."),
        ("💼", "Freelancer o servicio profesional", "Tienes un historial de clientes y proyectos. Quieres visualizar tu facturación y detectar tendencias para planificar mejor."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], perfiles):
        col.markdown(f"""
        <div style="
            border:1.5px solid #d0e8e9;
            border-radius:14px;
            padding:22px 20px;
            background:#f5fafa;
            height:100%;
            min-height:160px;
        ">
            <div style="font-size:32px;margin-bottom:10px;">{icon}</div>
            <div style="font-weight:700;color:#093134;font-size:15px;margin-bottom:8px;">{title}</div>
            <div style="color:#4a6e70;font-size:13.5px;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── ¿Cómo funciona? ──
    st.markdown("""
    <h2 style="color:#093134;font-weight:800;font-size:22px;margin-bottom:6px;">¿Cómo funciona?</h2>
    <p style="color:#4a6e70;font-size:15px;margin-bottom:24px;">Solo 3 pasos. Sin instalaciones, sin tutoriales, sin código.</p>
    """, unsafe_allow_html=True)
    
    s1, s2, s3 = st.columns(3)
    pasos = [
        ("01", "#5ec4c8", "Sube tu archivo", "CSV o Excel con tus registros de ventas. El sistema detecta automáticamente fechas, números y categorías."),
        ("02", "#6366f1", "Elige qué analizar", "Selecciona qué variable quieres medir (ej: Ventas) y con qué la quieres comparar (ej: Producto, Ciudad, Categoría)."),
        ("03", "#f59e0b", "Explora tus métricas", "Gráficas de barras, torta y evolución temporal interactivas listas al instante. Filtra por mes y descarga los datos."),
    ]
    for col, (num, color, title, desc) in zip([s1, s2, s3], pasos):
        col.markdown(f"""
        <div style="
            border:1.5px solid {color}33;
            border-radius:14px;
            padding:22px 20px;
            background:linear-gradient(135deg,{color}0a,#ffffff);
            height:100%;
            min-height:160px;
        ">
            <div style="
                display:inline-block;
                background:{color}22;
                color:{color};
                font-size:12px;
                font-weight:800;
                letter-spacing:0.1em;
                padding:3px 10px;
                border-radius:999px;
                margin-bottom:12px;
            ">PASO {num}</div>
            <div style="font-weight:700;color:#093134;font-size:15px;margin-bottom:8px;">{title}</div>
            <div style="color:#4a6e70;font-size:13.5px;line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Roadmap: Modelo Predictivo ──
    st.markdown("""
    <div style="
        border:1.5px solid #6366f133;
        border-radius:16px;
        padding:28px 32px;
        background:linear-gradient(135deg,#6366f108,#ffffff);
        margin-bottom:28px;
    ">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
            <span style="font-size:28px;">🔮</span>
            <div>
                <div style="font-size:16px;font-weight:800;color:#093134;">Modelo Predictivo de Ventas
                    <span style="
                        display:inline-block;
                        background:#f59e0b22;
                        color:#d97706;
                        font-size:11px;
                        font-weight:700;
                        padding:2px 10px;
                        border-radius:999px;
                        margin-left:10px;
                        letter-spacing:0.06em;
                    ">🚧 EN DESARROLLO</span>
                </div>
                <div style="color:#6b7280;font-size:13px;margin-top:2px;">Optimizando precisión con nuevos datos</div>
            </div>
        </div>
        <p style="color:#4a6e70;font-size:14.5px;line-height:1.7;margin:0 0 16px 0;">
            Hemos integrado un motor de <strong style="color:#093134;">Machine Learning (Random Forest)</strong> que aprende de tu historial
            para predecir tus ventas futuras. Constantemente estamos mejorando y ajustando la Inteligencia Artificial 
            para que sea capaz de capturar con mayor exactitud las <strong>estacionalidades, tendencias y patrones únicos</strong>
            de tu negocio.
        </p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <span style="background:#dcfce7;color:#16a34a;font-size:12px;font-weight:600;padding:4px 12px;border-radius:999px;">✅ Análisis histórico y tendencias</span>
            <span style="background:#fef3c7;color:#d97706;font-size:12px;font-weight:600;padding:4px 12px;border-radius:999px;">⏳ Mejora continua de predicciones</span>
            <span style="background:#ede9fe;color:#7c3aed;font-size:12px;font-weight:600;padding:4px 12px;border-radius:999px;">🔬 IA: Random Forest Activo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Sobre Selligent Labs ──
    st.markdown("""
    <div style="
        border:1.5px solid #d0e8e9;
        border-radius:16px;
        padding:24px 28px;
        background:#f5fafa;
        display:flex;
        align-items:flex-start;
        gap:20px;
    ">
        <div style="font-size:48px;flex-shrink:0;">🚀</div>
        <div>
            <div style="font-size:15px;font-weight:800;color:#093134;margin-bottom:6px;">Lleva tu negocio al siguiente nivel</div>
            <p style="color:#4a6e70;font-size:14px;line-height:1.7;margin:0;">
                <strong>Selligent Labs</strong> es una plataforma inteligente creada para <em>democratizar el análisis de datos</em>. 
                Nuestro objetivo es que cualquier emprendedor o dueño de negocio pueda tomar decisiones rentables 
                y respaldadas por Inteligencia Artificial, sin necesidad de lidiar con hojas de cálculo complejas o 
                contratar a un equipo técnico. ¡Sube tus datos y descubre el valor oculto en tus ventas!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
