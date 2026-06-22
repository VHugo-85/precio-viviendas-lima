"""
Módulo de entrenamiento y evaluación del modelo.
"""
import json
from pathlib import Path
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
def entrenar_modelo(
    X,
    y,
    n_estimators: int = 100,
    semilla: int = 42,
) -> Tuple[RandomForestRegressor, Dict[str, float]]:
    """Entrena un RandomForestRegressor y devuelve modelo y métricas."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=semilla,
    )
    modelo = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=semilla,
        n_jobs=-1,
    )
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    metricas = {
        "mae": round(float(mean_absolute_error(y_test, y_pred)), 2),
        "r2": round(float(r2_score(y_test, y_pred)), 4),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }
    return modelo, metricas

def guardar_metricas(metricas: Dict[str, float], ruta: str = "outputs/metrics.json") -> None:
    """Guarda métricas en formato JSON."""
    ruta_salida = Path(ruta)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(metricas, archivo, indent=2, ensure_ascii=False)
    print(f"Métricas guardadas en {ruta_salida}")
    print(json.dumps(metricas, indent=2, ensure_ascii=False))