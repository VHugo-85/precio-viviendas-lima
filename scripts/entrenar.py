"""
Script de entrenamiento completo.
Este script se ejecuta localmente y también desde GitHub Actions.
"""
from src.data_loader import generar_datos_lima
from src.model import entrenar_modelo, guardar_metricas
from src.preprocessing import (
    codificar_distrito,
    escalar_features,
    limpiar_datos,
    preparar_features_y_target,
)

def main() -> None:
    """Ejecuta el flujo completo de entrenamiento."""
    print("=== Iniciando entrenamiento ===")
    df = generar_datos_lima(n_muestras=500, semilla=42)
    print(f"Dataset generado: {df.shape}")
    df = limpiar_datos(df)
    df, _ = codificar_distrito(df)
    columnas_num = ["area_m2", "habitaciones", "banos", "antiguedad_anos"]
    df, _ = escalar_features(df, columnas_num)
    X, y = preparar_features_y_target(df)
    _, metricas = entrenar_modelo(X.values, y.values)
    guardar_metricas(metricas)
    print("=== Entrenamiento completo ===")

if __name__ == "__main__":
    main()