# Selligent Labs | Inteligencia de Negocios y Análisis Predictivo

Selligent Labs es una plataforma de análisis avanzado diseñada para transformar datos operativos en decisiones estratégicas. Orientada a pequeñas y medianas empresas (PYMES), la solución permite procesar registros históricos de ventas para generar visualizaciones interactivas de alto impacto y proyecciones comerciales basadas en inteligencia artificial, eliminando la barrera técnica del análisis de datos tradicional.

---

## Características Principales

### Procesamiento y Limpieza Automatizada
La plataforma integra un motor de detección de variables que identifica automáticamente formatos de fecha, valores numéricos y categorías. Incluye rutinas de normalización para limpiar símbolos de moneda, separadores de miles y caracteres especiales, permitiendo la ingesta de archivos CSV y Excel sin preparación previa.

### Análisis de Ventas de Alta Fidelidad
Proporciona un tablero de control con indicadores clave de rendimiento (KPIs) dinámicos:
* Análisis de ingresos totales y ticket promedio.
* Identificación de tendencias operacionales y estacionalidad.
* Mapas de calor para la detección de picos de demanda intradía y semanal.
* Desglose por categorías líderes y rendimiento de inventario.

### Motor de Proyección Comercial
Utiliza algoritmos de aprendizaje automático (Random Forest) para modelar el comportamiento futuro de las ventas. 
* Implementa validación temporal (Walk-Forward Validation) para asegurar la precisión del modelo.
* Realiza proyecciones a 7 días basadas en patrones históricos de demanda.
* Proporciona un índice de confianza basado en el error medio absoluto porcentual (MAPE).
* Sustituye la terminología técnica compleja por indicadores de negocio comprensibles para el usuario final.

### Interfaz de Usuario Premium
Diseñada bajo una estética de alto rendimiento, la interfaz utiliza:
* Fondos dinámicos y arquitectura visual basada en capas (Glassmorphism).
* Gráficos interactivos de alto rendimiento mediante la integración de Apache ECharts.
* Animaciones fluidas y retroalimentación interactiva en tiempo real.

---

## Arquitectura Tecnológica

* **Lenguaje:** Python 3.9+
* **Interfaz de Usuario:** Streamlit con inyección de CSS y HTML5 personalizado.
* **Procesamiento de Datos:** Pandas y NumPy.
* **Visualización de Datos:** Streamlit-ECharts.
* **Aprendizaje Automático:** Scikit-Learn (Random Forest Regressor).
* **Validación de Modelos:** TimeSeriesSplit para validación cruzada temporal.

---

## Instalación y Configuración

Siga estos pasos para ejecutar la plataforma en un entorno local:

1. **Clonación del repositorio:**
   ```bash
   git clone https://github.com/su-usuario/selligent-labs.git
   cd selligent-labs
   ```

2. **Configuración del entorno virtual:**
   ```bash
   python -m venv venv
   # Activación en Windows:
   .\venv\Scripts\activate
   # Activación en macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalación de dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecución de la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

## Metodología de Predicción

El sistema de predicción inteligente no se limita a proyecciones lineales. El motor realiza un proceso de ingeniería de características automático que considera:
1. **Componentes Temporales:** Día de la semana, mes y estacionalidad.
2. **Variables de Retraso (Lags):** Comportamiento de los últimos 1, 2, 3 y 7 días para capturar dependencias a corto plazo.
3. **Estadísticas Móviles:** Promedios y desviaciones estándar rodantes para identificar cambios en la volatilidad.
4. **Optimización:** Ajuste automático de hiperparámetros para adaptar el modelo a la escala y volumen específico de cada negocio.

---
**Selligent Labs** | Transformando datos en crecimiento comercial.
