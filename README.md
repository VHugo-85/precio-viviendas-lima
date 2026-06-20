# precio-viviendas-lima
Modelo de Machine Learning para predecir el precio de viviendas en Lima
Metropolitana.
Este repositorio forma parte del proyecto final del curso **GitHub para Producción
en Data Science** del Instituto de Analítica y Negocios.
## Objetivo del proyecto
Construir un repositorio profesional de Data Science usando GitHub, GitHub Actions,
Pull Requests, releases, herramientas de seguridad y consulta mediante API.
El modelo usa datos sintéticos de viviendas en Lima. El objetivo principal no es
obtener el mejor modelo posible, sino practicar un flujo profesional de trabajo
con GitHub.
## Tecnologías utilizadas
- Python 3.10+
- pandas
- numpy
- scikit-learn
- pytest
- GitHub Actions
- PyGitHub
## Instalación
Clona el repositorio:
```bash
git clone git@github.com:TU-USUARIO/precio-viviendas-lima.git
cd precio-viviendas-lima
```
Crea y activa el entorno virtual:
```bash
python -m venv .venv
source .venv/Scripts/activate
```
Instala dependencias:
```bash
python -m pip install -r requirements.txt
```
## Uso rápido
```python
from src.data_loader import generar_datos_lima
df = generar_datos_lima()
print(df.head())
```
## Ejecutar tests
```bash
python -m pytest tests/ -v
```
## Ejecutar entrenamiento
```bash
python -m scripts.entrenar
```
## Estructura general
```text
src/ Código fuente del proyecto
tests/ Tests automáticos
scripts/ Scripts ejecutables
docs/ Documentación metodológica
outputs/ Resultados generados localmente
.github/ Workflows y configuración de GitHub
```
## Nota
El archivo `outputs/metrics.json` se genera localmente o dentro de GitHub Actions,
pero no se sube al repositorio porque está ignorado por `.gitignore`.