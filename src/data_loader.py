"""
Módulo para generar datos sintéticos de viviendas en Lima.
Este archivo simula un pequeño dataset para practicar GitHub,
GitHub Actions y organización de proyectos de Data Science.
"""
import numpy as np
import pandas as pd
def generar_datos_lima(n_muestras: int = 200, semilla: int = 42) -> pd.DataFrame:
    """Genera un dataset sintético de viviendas en Lima.
    Parameters
    ----------
    n_muestras : int
        Número de filas que tendrá el dataset.
    semilla : int
        Semilla para obtener resultados reproducibles.
    Returns
    -------
    pd.DataFrame
        DataFrame con variables de vivienda y precio estimado.
    """
    rng = np.random.default_rng(semilla)
    distritos = [
        "Miraflores",
        "San Isidro",
        "Surco",
        "Barranco",
        "La Molina",
        "Jesús María",
        "Lince",
        "Pueblo Libre",
    ]
    precios_base = {
        "Miraflores": 3200,
        "San Isidro": 3500,
        "Surco": 2800,
        "Barranco": 2900,
        "La Molina": 2600,
        "Jesús María": 2200,
        "Lince": 2000,
        "Pueblo Libre": 2100,
    }
    distrito_col = rng.choice(distritos, size=n_muestras)
    area = rng.integers(40, 250, size=n_muestras).astype(float)
    habitaciones = rng.integers(1, 6, size=n_muestras)
    banos = rng.integers(1, 4, size=n_muestras)
    antiguedad = rng.integers(0, 40, size=n_muestras).astype(float)
    precio = np.array(
        [
            precios_base[d] * area[i]
            * (1 + 0.05 * habitaciones[i])
            * (1 - 0.005 * antiguedad[i])
            + rng.normal(0, 15000)
            for i, d in enumerate(distrito_col)
        ]
    )
    return pd.DataFrame(
        {
            "distrito": distrito_col,
            "area_m2": area,
            "habitaciones": habitaciones,
            "banos": banos,
            "antiguedad_anos": antiguedad,
            "precio_usd": precio.round(2),
        }
    )

if __name__ == "__main__":
    df = generar_datos_lima()
    print(f"Dataset generado: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(df.head())