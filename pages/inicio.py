import streamlit as st

def mostrar_inicio():

    # ── HERO SECTION ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @keyframes fadeUp   { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
    @keyframes shimmer  { 0%,100% { opacity:.6; } 50% { opacity:1; } }
    @keyframes floatOrb { 0%,100% { transform:translateY(0) scale(1); } 50% { transform:translateY(-18px) scale(1.04); } }
    @keyframes pulse    { 0%,100% { box-shadow:0 0 0 0 rgba(94,196,200,.45); } 70% { box-shadow:0 0 0 14px rgba(94,196,200,0); } }
    @keyframes ticker   { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
    @keyframes gradMove { 0%,100% { background-position:0% 50%; } 50% { background-position:100% 50%; } }

    .hero-wrap {
        background: linear-gradient(135deg, #062527 0%, #093134 40%, #0d4a4e 70%, #1a6f75 100%);
        background-size: 200% 200%;
        animation: gradMove 8s ease-in-out infinite;
        border-radius: 24px;
        padding: 60px 56px 52px 56px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(94,196,200,0.2);
    }
    .hero-orb-1 {
        position:absolute; top:-80px; right:-80px;
        width:340px; height:340px; border-radius:50%;
        background: radial-gradient(circle, rgba(94,196,200,0.12) 0%, transparent 70%);
        animation: floatOrb 7s ease-in-out infinite;
    }
    .hero-orb-2 {
        position:absolute; bottom:-100px; right:200px;
        width:220px; height:220px; border-radius:50%;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
        animation: floatOrb 9s ease-in-out infinite reverse;
    }
    .hero-orb-3 {
        position:absolute; top:60px; left:-60px;
        width:180px; height:180px; border-radius:50%;
        background: radial-gradient(circle, rgba(245,158,11,0.07) 0%, transparent 70%);
        animation: floatOrb 11s ease-in-out infinite;
    }
    .hero-badge {
        display:inline-flex; align-items:center; gap:7px;
        background: rgba(94,196,200,0.15);
        color: #7dd9dd;
        font-size:11px; font-weight:700; letter-spacing:.14em;
        text-transform:uppercase; padding:5px 16px;
        border-radius:999px; border:1px solid rgba(94,196,200,0.3);
        margin-bottom:26px;
        animation: fadeUp .6s ease both;
    }
    .hero-title {
        font-size: clamp(40px,5vw,62px);
        font-weight:900; color:#fff; letter-spacing:-.035em; line-height:1.05;
        margin:0 0 8px 0;
        animation: fadeUp .7s ease .1s both;
    }
    .hero-title-accent { color:#5ec4c8; }
    .hero-subtitle {
        font-size: clamp(18px,2.2vw,24px);
        font-weight:700; color:#b0e0e2; letter-spacing:-.01em;
        margin:0 0 18px 0;
        animation: fadeUp .7s ease .2s both;
    }
    .hero-body {
        color:#cce8ea; font-size:16px; line-height:1.85;
        max-width:640px; font-weight:400;
        animation: fadeUp .7s ease .3s both;
    }
    .hero-body strong { color:#5ec4c8; font-weight:700; }
    .hero-cta {
        display:inline-flex; align-items:center; gap:10px;
        background: linear-gradient(135deg,#5ec4c8,#3ea8ac);
        color:#fff; font-size:15px; font-weight:700;
        padding:14px 30px; border-radius:12px;
        margin-top:28px; cursor:pointer;
        box-shadow: 0 8px 24px rgba(94,196,200,0.4);
        animation: fadeUp .7s ease .4s both, pulse 2.5s 1.5s infinite;
        border:none; text-decoration:none;
    }

    /* ── Stats bar ── */
    .stats-bar {
        display:flex; gap:0; background:#fff;
        border-radius:16px; overflow:hidden;
        box-shadow:0 4px 24px rgba(0,0,0,0.08);
        margin-bottom:44px;
        border:1px solid #e5e7eb;
    }
    .stat-item {
        flex:1; text-align:center; padding:22px 16px;
        border-right:1px solid #f0f0f0;
        transition: background .25s;
    }
    .stat-item:last-child { border-right:none; }
    .stat-item:hover { background:#f0fafa; }
    .stat-num {
        font-size:28px; font-weight:900; color:#093134;
        letter-spacing:-.03em; line-height:1;
        margin-bottom:4px;
    }
    .stat-num span { color:#5ec4c8; }
    .stat-label { font-size:12px; color:#6b7280; font-weight:600; text-transform:uppercase; letter-spacing:.06em; }

    /* ── Section titles ── */
    .sec-eyebrow {
        display:inline-block;
        background:#ecfdf5; color:#059669;
        font-size:11px; font-weight:700; letter-spacing:.12em;
        text-transform:uppercase; padding:4px 14px; border-radius:999px;
        margin-bottom:10px;
    }
    .sec-eyebrow.purple { background:#ede9fe; color:#7c3aed; }
    .sec-eyebrow.amber  { background:#fef3c7; color:#d97706; }
    .sec-eyebrow.blue   { background:#eff6ff; color:#2563eb; }
    .sec-title {
        font-size:26px; font-weight:900; color:#093134;
        letter-spacing:-.025em; margin:0 0 8px 0;
    }
    .sec-sub { font-size:15px; color:#6b7280; margin:0 0 30px 0; line-height:1.6; }

    /* ── Profile cards (quién es) ── */
    .profile-grid {
        display:grid; grid-template-columns:repeat(3,1fr); gap:16px;
        margin-bottom:48px;
    }
    .profile-card {
        background:#fff; border-radius:16px;
        border:1.5px solid #e8f0f1;
        padding:24px 20px;
        transition: all .25s ease;
        position:relative; overflow:hidden;
    }
    .profile-card::before {
        content:''; position:absolute; top:0; left:0; right:0; height:4px;
        background: var(--card-accent, #5ec4c8);
        border-radius:16px 16px 0 0;
    }
    .profile-card:hover {
        border-color: var(--card-accent, #5ec4c8);
        box-shadow: 0 8px 28px rgba(0,0,0,0.09);
        transform: translateY(-4px);
    }
    .profile-icon {
        width:52px; height:52px; border-radius:14px;
        background: var(--card-bg, #f0fafa);
        display:flex; align-items:center; justify-content:center;
        font-size:26px; margin-bottom:14px;
    }
    .profile-title { font-size:15px; font-weight:800; color:#093134; margin-bottom:6px; }
    .profile-desc  { font-size:13px; color:#6b7280; line-height:1.65; }

    /* ── How-it-works ── */
    .steps-wrap {
        display:grid; grid-template-columns:1fr 40px 1fr 40px 1fr; gap:0;
        align-items:center; margin-bottom:48px;
    }
    .step-card {
        background:#fff; border-radius:18px; padding:28px 22px;
        border:1.5px solid #e8f0f1;
        text-align:center; position:relative;
        transition: box-shadow .25s, transform .25s;
    }
    .step-card:hover { box-shadow:0 10px 32px rgba(0,0,0,0.1); transform:translateY(-4px); }
    .step-num {
        width:44px; height:44px; border-radius:12px;
        background: var(--step-color); color:#fff;
        font-size:16px; font-weight:900;
        display:flex; align-items:center; justify-content:center;
        margin:0 auto 14px auto;
        box-shadow: 0 4px 12px color-mix(in srgb, var(--step-color) 40%, transparent);
    }
    .step-arrow {
        text-align:center; font-size:22px; color:#d1d5db;
        animation: shimmer 2s ease-in-out infinite;
    }
    .step-title { font-size:15px; font-weight:800; color:#093134; margin-bottom:8px; }
    .step-desc  { font-size:13px; color:#6b7280; line-height:1.65; }

    /* ── Feature grid ── */
    .feat-grid {
        display:grid; grid-template-columns:repeat(4,1fr); gap:14px;
        margin-bottom:48px;
    }
    .feat-card {
        background:#fff; border-radius:14px;
        border:1.5px solid #f0f0f0; padding:20px 18px;
        transition: all .2s;
    }
    .feat-card:hover { border-color:#5ec4c8; box-shadow:0 6px 20px rgba(94,196,200,.18); transform:translateY(-3px); }
    .feat-icon { font-size:24px; margin-bottom:10px; }
    .feat-title { font-size:14px; font-weight:700; color:#111827; margin-bottom:5px; }
    .feat-desc  { font-size:12.5px; color:#6b7280; line-height:1.6; }

    /* ── CTA bottom ── */
    .cta-bottom {
        background: linear-gradient(135deg,#093134 0%,#1a6f75 100%);
        border-radius:20px; padding:44px 52px;
        text-align:center; position:relative; overflow:hidden;
        border:1px solid rgba(94,196,200,0.2);
        margin-bottom:12px;
    }
    .cta-bottom-orb {
        position:absolute; border-radius:50%;
        background:rgba(94,196,200,0.07);
    }
    .cta-title { font-size:28px; font-weight:900; color:#fff; letter-spacing:-.025em; margin-bottom:10px; }
    .cta-sub   { font-size:16px; color:#b0e0e2; margin-bottom:26px; max-width:520px; margin-left:auto; margin-right:auto; }
    .cta-btn {
        display:inline-flex; align-items:center; gap:8px;
        background:#5ec4c8; color:#fff; font-weight:700; font-size:15px;
        padding:14px 32px; border-radius:12px;
        box-shadow:0 6px 20px rgba(94,196,200,.45);
        transition: all .2s; cursor:pointer; text-decoration:none;
    }
    .cta-btn:hover { background:#4eb0b4; transform:translateY(-2px); }

    /* ── Responsive tweaks ── */
    @media (max-width:900px) {
        .profile-grid { grid-template-columns:1fr 1fr; }
        .feat-grid    { grid-template-columns:1fr 1fr; }
        .steps-wrap   { grid-template-columns:1fr; }
        .step-arrow   { display:none; }
    }
    </style>

    <!-- ═══════════════ HERO ═══════════════ -->
    <div class="hero-wrap">
        <div class="hero-orb-1"></div>
        <div class="hero-orb-2"></div>
        <div class="hero-orb-3"></div>
        <div style="position:relative;z-index:1;">
            <div class="hero-badge sl-banner-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                Inteligencia para tu Negocio 
            </div>
            <div class="hero-title">Tu negocio habla.<br><span class="hero-title-accent">Selligent Labs</span> lo traduce.</div>
            <div class="hero-subtitle">De tus datos de ventas a decisiones rentables — en minutos.</div>
            <p class="hero-body">
                Sube tu archivo de ventas (CSV o Excel) y en segundos obtienes
                <strong>dashboards interactivos, análisis de tendencias y predicciones con IA</strong>.
                Sin código. Sin analistas. Sin Power BI. Diseñado para que cualquier dueño de negocio
                entienda sus números y tome mejores decisiones.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATS BAR ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-num">3<span>min</span></div>
            <div class="stat-label">De datos a insights</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">0<span>$</span></div>
            <div class="stat-label">Costo de analista</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">+<span>15</span></div>
            <div class="stat-label">Métricas automáticas</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">100<span>%</span></div>
            <div class="stat-label">Sin instalación</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">IA<span> ✓</span></div>
            <div class="stat-label">Predicción incluida</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ¿PARA QUIÉN? ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:30px;">
        <div class="sec-eyebrow">Para todo tipo de PYME</div>
        <div class="sec-title">¿Tu negocio vende? Esto es para ti.</div>
        <div class="sec-sub">Sin importar el sector. Si tienes datos de ventas, Selligent Labs los convierte en oportunidades.</div>
    </div>

    <div class="profile-grid">
        <div class="profile-card" style="--card-accent:#5ec4c8;--card-bg:#f0fafa;">
            <div class="profile-icon">🛍️</div>
            <div class="profile-title">Tienda física o e-commerce</div>
            <div class="profile-desc">Exporta desde tu POS o Shopify y descubre qué productos generan más margen, cuándo compran tus clientes y cómo crecer mes a mes.</div>
        </div>
        <div class="profile-card" style="--card-accent:#6366f1;--card-bg:#f5f3ff;">
            <div class="profile-icon">🍽️</div>
            <div class="profile-title">Restaurante o café</div>
            <div class="profile-desc">Identifica tus días pico, platillos estrella y temporadas bajas para planificar mejor tu menú, personal y promociones.</div>
        </div>
        <div class="profile-card" style="--card-accent:#f59e0b;--card-bg:#fffbeb;">
            <div class="profile-icon">💼</div>
            <div class="profile-title">Servicios profesionales</div>
            <div class="profile-desc">Consultores, agencias y freelancers que quieren visualizar su facturación, detectar clientes clave y proyectar ingresos futuros.</div>
        </div>
        <div class="profile-card" style="--card-accent:#10b981;--card-bg:#f0fdf4;">
            <div class="profile-icon">🏗️</div>
            <div class="profile-title">Distribuidoras y mayoristas</div>
            <div class="profile-desc">Analiza tus líneas de producto, rutas o clientes corporativos para optimizar inventarios y enfocar a tu equipo comercial.</div>
        </div>
        <div class="profile-card" style="--card-accent:#ef4444;--card-bg:#fef2f2;">
            <div class="profile-icon">🏥</div>
            <div class="profile-title">Clínicas y salud</div>
            <div class="profile-desc">Lleva el control de atenciones, servicios y facturación mensual para tomar decisiones operativas y de crecimiento respaldadas en datos.</div>
        </div>
        <div class="profile-card" style="--card-accent:#8b5cf6;--card-bg:#faf5ff;">
            <div class="profile-icon">🎓</div>
            <div class="profile-title">Educación y formación</div>
            <div class="profile-desc">Academias, institutos y capacitadores que quieren analizar inscripciones, cursos más vendidos y proyectar demanda futura.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CÓMO FUNCIONA ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:30px;">
        <div class="sec-eyebrow purple">Proceso simple</div>
        <div class="sec-title">3 pasos. 0 complicaciones.</div>
        <div class="sec-sub">Sin instalaciones, sin tutoriales técnicos, sin código. Solo sube y explora.</div>
    </div>

    <div class="steps-wrap">
        <div class="step-card" style="--step-color:#5ec4c8;">
            <div class="step-num" style="--step-color:#5ec4c8;">01</div>
            <div style="font-size:32px;margin-bottom:12px;">📂</div>
            <div class="step-title">Sube tu archivo</div>
            <div class="step-desc">CSV o Excel con tus registros de ventas. Detectamos automáticamente fechas, montos y categorías. Cualquier formato funciona.</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card" style="--step-color:#6366f1;">
            <div class="step-num" style="--step-color:#6366f1;">02</div>
            <div style="font-size:32px;margin-bottom:12px;">⚙️</div>
            <div class="step-title">Configura tu análisis</div>
            <div class="step-desc">Selecciona qué métrica medir (ventas, unidades) y cómo segmentarla (producto, categoría, ciudad). Sin código, solo clics.</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card" style="--step-color:#f59e0b;">
            <div class="step-num" style="--step-color:#f59e0b;">03</div>
            <div style="font-size:32px;margin-bottom:12px;">🚀</div>
            <div class="step-title">Obtén tus insights</div>
            <div class="step-desc">Gráficas interactivas, KPIs inteligentes, heatmaps semanales y predicciones con IA listos al instante. Filtra, explora y decide.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CARACTERÍSTICAS ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:30px;">
        <div class="sec-eyebrow blue">Funcionalidades</div>
        <div class="sec-title">Todo lo que necesitas para conocer tu negocio</div>
    </div>

    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon">📊</div>
            <div class="feat-title">KPIs automáticos</div>
            <div class="feat-desc">Ventas totales, ticket promedio, días activos, máximos y mínimos calculados al instante con comparativa vs. mes anterior.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📅</div>
            <div class="feat-title">Heatmap semanal</div>
            <div class="feat-desc">Visualiza exactamente qué días de la semana generan más ingresos para planificar personal, inventario y promociones.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📈</div>
            <div class="feat-title">Evolución temporal</div>
            <div class="feat-desc">Gráfica de línea interactiva con zoom, filtro por mes y detección automática de tendencia (creciente, estable o a la baja).</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🥧</div>
            <div class="feat-title">Análisis de categorías</div>
            <div class="feat-desc">Barras y tortas comparativas de tus productos, servicios o categorías. Identifica tu motor de ingresos en segundos.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🤖</div>
            <div class="feat-title">Resumen con IA</div>
            <div class="feat-desc">El sistema genera automáticamente interpretaciones en lenguaje natural de tus indicadores, sin que tengas que leer tablas.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🔮</div>
            <div class="feat-title">Predicción de ventas</div>
            <div class="feat-desc">Modelo de Machine Learning (Random Forest) que aprende de tu historial y proyecta tus ventas futuras con intervalos de confianza.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📁</div>
            <div class="feat-title">Cualquier formato</div>
            <div class="feat-desc">Compatible con CSV y Excel. Detecta automáticamente el separador, la codificación y el formato de fechas de tu archivo.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🔒</div>
            <div class="feat-title">Tus datos, tu control</div>
            <div class="feat-desc">Los datos se procesan en memoria durante tu sesión. Nada se guarda en servidores externos. Tu información es solo tuya.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA FINAL ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-bottom">
        <div class="cta-bottom-orb" style="width:280px;height:280px;top:-120px;right:-80px;"></div>
        <div class="cta-bottom-orb" style="width:180px;height:180px;bottom:-80px;left:60px;"></div>
        <div style="position:relative;z-index:1;">
            <div style="font-size:36px;margin-bottom:16px;">🚀</div>
            <div class="cta-title">¿Listo para conocer tu negocio de verdad?</div>
            <div class="cta-sub">
                Miles de decisiones se toman a ciegas cada día en las PYMES. Las tuyas no tienen por qué serlo.
                Sube tu primer archivo ahora — es económico, inmediato y no requiere registro.
            </div>
        </div>
    </div>

    <div style="text-align:center;margin-top:20px;padding-bottom:8px;">
        <span style="font-size:13px;color:#9ca3af;font-weight:500;">
             <strong style="color:#5ec4c8;">Selligent Labs</strong> · Inteligencia de Negocios
        </span>
    </div>
    """, unsafe_allow_html=True)
