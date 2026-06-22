"""
Módulo de preprocesamiento para el dataset de viviendas.
"""
from typing import List, Tuple
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina registros incompletos y valores imposibles."""
    df = df.copy()
    df = df.dropna()
    df = df[df["precio_usd"] > 0]
    df = df[df["area_m2"] > 0]
    return df.reset_index(drop=True)
def codificar_distrito(df: pd.DataFrame) -> Tuple[pd.DataFrame, LabelEncoder]:
    """Convierte la columna distrito en una columna numérica."""
    df = df.copy()
    encoder = LabelEncoder()
    df["distrito_cod"] = encoder.fit_transform(df["distrito"])
    df = df.drop(columns=["distrito"])
    return df, encoder

def escalar_features(
    df: pd.DataFrame, columnas: List[str]
) -> Tuple[pd.DataFrame, StandardScaler]:
    """Estandariza columnas numéricas usando StandardScaler."""
    df = df.copy()
    scaler = StandardScaler()
    df[columnas] = scaler.fit_transform(df[columnas])
    return df, scaler
def preparar_features_y_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separa variables predictoras y variable objetivo."""
    target = "precio_usd"
    features = [col for col in df.columns if col != target]
    return df[features], df[target]