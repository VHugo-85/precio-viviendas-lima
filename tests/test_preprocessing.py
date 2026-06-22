"""
Tests automáticos para el módulo de preprocesamiento.
"""
import pandas as pd
import pytest
from sklearn.preprocessing import LabelEncoder
from src.data_loader import generar_datos_lima
from src.preprocessing import (
    codificar_distrito,
    escalar_features,
    limpiar_datos,
    preparar_features_y_target,
)

@pytest.fixture
def df_base() -> pd.DataFrame:
    """Dataset base para las pruebas."""
    return generar_datos_lima(n_muestras=50, semilla=0)
def test_limpiar_datos_no_pierde_filas_limpias(df_base):
    resultado = limpiar_datos(df_base)
    assert len(resultado) == len(df_base)

def test_limpiar_datos_elimina_precio_negativo(df_base):
    df_sucio = df_base.copy()
    df_sucio.loc[0, "precio_usd"] = -1000
    resultado = limpiar_datos(df_sucio)
    assert len(resultado) == len(df_base) - 1
    assert (resultado["precio_usd"] > 0).all()

def test_codificar_distrito_crea_columna(df_base):
    resultado, _ = codificar_distrito(df_base)
    assert "distrito_cod" in resultado.columns
    assert "distrito" not in resultado.columns

def test_codificar_distrito_retorna_encoder(df_base):
    _, encoder = codificar_distrito(df_base)
    assert isinstance(encoder, LabelEncoder)

def test_escalar_features_media_cero(df_base):
    df_limpio = limpiar_datos(df_base)
    columnas = ["area_m2", "antiguedad_anos"]
    resultado, _ = escalar_features(df_limpio, columnas)
    for col in columnas:
        assert abs(resultado[col].mean()) < 1e-10

def test_preparar_features_y_target_shape(df_base):
    df_limpio = limpiar_datos(df_base)
    df_codificado, _ = codificar_distrito(df_limpio)
    X, y = preparar_features_y_target(df_codificado)
    assert X.shape[1] == df_codificado.shape[1] - 1
    assert len(y) == len(df_codificado)