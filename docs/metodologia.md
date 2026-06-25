# Metodología del modelo
## Contexto
Este proyecto usa un dataset sintético de viviendas en Lima Metropolitana. Los
datos fueron generados con fines académicos para practicar GitHub, GitHub
Actions y automatización de proyectos de Data Science.
## Variables de entrada
| Variable | Tipo | Descripción |
|---|---|---|
| `area_m2` | Numérica | Área de la vivienda en metros cuadrados. |
| `habitaciones` | Entera | Número de habitaciones. |
| `banos` | Entera | Número de baños. |
| `antiguedad_anos` | Numérica | Antigüedad de la vivienda en años. |
| `distrito_cod` | Entera | Distrito convertido a código numérico. |
## Variable objetivo
| Variable | Descripción |
|---|---|
| `precio_usd` | Precio estimado de la vivienda en dólares americanos. |
## Preprocesamiento
El flujo de preprocesamiento incluye:
1. Eliminación de valores nulos.
2. Eliminación de precios negativos.
3. Eliminación de áreas no válidas.
4. Codificación numérica del distrito.
5. Escalamiento de variables numéricas.
## Modelo utilizado
Se utiliza `RandomForestRegressor` de scikit-learn.
Este modelo combina varios árboles de decisión para producir una predicción más
estable que un único árbol individual.
## Métricas de evaluación
| Métrica | Significado |
|---|---|
| MAE | Error absoluto medio expresado en dólares. |
| R2 | Proporción de variabilidad explicada por el modelo. |
## Limitaciones
- El dataset es sintético.
- Las métricas no representan el mercado inmobiliario real de Lima.
- El objetivo principal del proyecto es practicar GitHub, no construir un modelo
inmobiliario productivo.