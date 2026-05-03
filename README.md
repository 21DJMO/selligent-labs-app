# 🚀 Selligent Labs | Inteligencia para tu negocio

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-2ca02c.svg)

**Selligent Labs** es una plataforma inteligente diseñada para democratizar el análisis de datos. Permite a dueños de negocios, emprendedores y pequeñas empresas subir sus registros históricos de ventas (Excel o CSV) para obtener visualizaciones interactivas al instante y **proyecciones de ventas futuras** impulsadas por algoritmos de Machine Learning, todo sin requerir conocimientos técnicos ni equipos especializados.

---

## ✨ Características Principales

* **🪄 Carga y Detección Inteligente:** Sube un archivo CSV o Excel y el sistema detectará automáticamente qué columnas son fechas, valores numéricos o categorías (incluso limpia formatos de moneda irregulares).
* **📊 Visualizaciones Dinámicas y Premium:** Genera análisis interactivos con gráficos de ECharts (barras, tortas, líneas de tiempo ajustables) en una interfaz moderna y estética.
* **🔮 Motor Predictivo con IA:** Un algoritmo interno de **Random Forest** entrena sobre la marcha con tus datos. Analiza patrones complejos (días de la semana, rachas, histórico) para calcular con precisión una proyección de ingresos para los próximos 7 días, mostrándote el "Nivel de Confianza" de la predicción.
* **💎 Interfaz (UX/UI) Fricción Cero:** Oculta por completo la complejidad matemática detrás de tarjetas estéticas, colores relajantes y explicaciones en lenguaje cotidiano. 

## 🛠️ Tecnologías Utilizadas

* **Framework Web:** [Streamlit](https://streamlit.io/)
* **Manipulación de Datos:** Pandas, Numpy
* **Gráficos interactivos:** Streamlit-ECharts
* **Machine Learning:** Scikit-Learn (`RandomForestRegressor`)
* **Diseño:** CSS personalizado, HTML inyectado y animaciones SVG nativas.

## ⚙️ Instalación y Uso Local

Para correr este proyecto en tu propia máquina:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/selligent-labs.git
   cd selligent-labs
   ```

2. **Crea un entorno virtual (Opcional pero recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicia el Dashboard:**
   ```bash
   streamlit run nuevo_dashboard.py
   ```
   *La aplicación se abrirá automáticamente en tu navegador web en `http://localhost:8501`.*

## 🧠 Detrás del Motor Predictivo

A diferencia de dashboards tradicionales, el módulo **Predicción Inteligente** realiza *Feature Engineering* automático en background:
1. Limita el ruido estadístico enfocándose en los últimos 90 días del negocio.
2. Crea variables predictivas como: `día de la semana`, `lag de 1, 2, 3 y 7 días`, y `promedio móvil de 7 días`.
3. Entrena un modelo de 100 árboles de decisión que aprende cómo fluctúan las ventas específicamente para ese negocio en particular.
4. Ejecuta proyecciones recursivas mostrando ingresos futuros viables en vez de suposiciones lineales genéricas.

---
**¿Quieres llevar tu negocio al siguiente nivel?** Empieza a descubrir el valor oculto en tus ventas hoy mismo.
