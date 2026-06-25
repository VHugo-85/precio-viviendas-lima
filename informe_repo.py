"""
informe_repo.py - Reporte automático del repositorio con PyGitHub.
Uso:
    python informe_repo.py
Requiere:
    - Archivo .env con GH_TOKEN y GITHUB_REPO.
    - Dependencias instaladas desde requirements.txt.
Nota:
    El archivo outputs/metrics.json se lee localmente si existe.
    No se busca en GitHub porque está ignorado por .gitignore.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from github import Github, GithubException

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO")

if not TOKEN:
    raise EnvironmentError("Variable GH_TOKEN no encontrada. Revisa tu archivo .env")

if not REPO_NAME:
    raise EnvironmentError("Variable GITHUB_REPO no encontrada. Revisa tu archivo .env")


def separador(titulo: str) -> None:
    """Imprime un separador visual limpio."""
    ancho = 70
    print(f"\n{'-' * ancho}")
    print(f" 📦 {titulo}")
    print(f"{'-' * ancho}")


def formatear_numero(valor: Any, decimales: int = 2) -> str:
    """Formatea números de manera segura."""
    if isinstance(valor, (int, float)):
        return f"{valor:,.{decimales}f}"
    return "N/A"


def mostrar_metricas_locales() -> None:
    """Muestra métricas si existe outputs/metrics.json localmente."""
    ruta_metricas = Path("outputs/metrics.json")

    if not ruta_metricas.exists():
        print(" ⚠️ No se encontró outputs/metrics.json en tu máquina.")
        print(" Ejecuta: python -m scripts.entrenar")
        return

    try:
        with open(ruta_metricas, "r", encoding="utf-8") as archivo:
            metricas = json.load(archivo)
        print(f" 📉 MAE: {formatear_numero(metricas.get('mae'))} USD")
        print(f" 📈 R2: {formatear_numero(metricas.get('r2'), 4)}")
        print(f" 📊 Train: {metricas.get('n_train', 'N/A')} muestras")
        print(f" 🧪 Test: {metricas.get('n_test', 'N/A')} muestras")
    except json.JSONDecodeError:
        print(" ❌ El archivo outputs/metrics.json está corrupto o mal formateado.")


def main() -> None:
    """Genera el informe del repositorio."""
    github_client = Github(TOKEN)

    try:
        repo = github_client.get_repo(REPO_NAME)
    except GithubException as exc:
        github_client.close()
        raise RuntimeError(
            "No se pudo acceder al repositorio. "
            "Verifica GITHUB_REPO y los permisos del token."
        ) from exc

    # Encabezado Principal
    print(f"\n{'=' * 70}")
    print(f" 📊 INFORME DEL REPOSITORIO: {repo.name.upper()}")
    print(f" 🕒 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 70}")

    # 1. INFORMACIÓN GENERAL
    separador("INFORMACIÓN GENERAL")
    print(f" 🏠 Repositorio: {repo.full_name}")
    print(f" 📝 Descripción: {repo.description or 'Sin descripción'}")
    print(f" 🌿 Rama default: {repo.default_branch}")
    print(f" ⭐ Estrellas: {repo.stargazers_count}")
    print(f" 🍴 Forks: {repo.forks_count}")
    print(f" 🐛 Issues abiertos: {repo.open_issues_count}")

    # 2. ÚLTIMOS COMMITS
    separador("ÚLTIMOS 5 COMMITS")
    try:
        commits = list(repo.get_commits()[:5])
        if not commits:
            print(" 💬 No se encontraron commits.")
        else:
            for commit in commits:
                sha = commit.sha[:7]
                mensaje = commit.commit.message.split("\n")[0]
                autor = commit.commit.author.name if commit.commit.author else "Desconocido"
                fecha = commit.commit.author.date.strftime("%Y-%m-%d") if commit.commit.author else "S/F"
                print(f" 🚀 [{sha}] {fecha} • {autor}")
                print(f"    {mensaje}")
    except GithubException:
        print(" ❌ No se pudieron cargar los commits.")

    # 3. ISSUES ABIERTOS (CORREGIDA INDENTACIÓN)
    separador("ISSUES ABIERTOS")
    try:
        issues = [
            issue for issue in repo.get_issues(state="open")
            if issue.pull_request is None
        ]
        if not issues:
            print(" ✅ No hay issues abiertos.")
        else:
            for issue in issues:
                etiquetas = ", ".join(label.name for label in issue.labels) or "sin etiqueta"
                fecha = issue.created_at.strftime("%Y-%m-%d")
                print(f" 📌 #{issue.number} {issue.title}")
                print(f"    Etiquetas: {etiquetas} | Abierto: {fecha}")
    except GithubException:
        print(" ❌ No se pudieron cargar los issues.")

    # 4. WORKFLOWS (CORREGIDA INDENTACIÓN)
    separador("ÚLTIMAS EJECUCIONES DE WORKFLOWS")
    try:
        workflows = list(repo.get_workflows())
        if not workflows:
            print(" ⚙️ No se encontraron workflows.")
        else:
            for workflow in workflows:
                runs = list(workflow.get_runs()[:2])
                if not runs:
                    continue

                print(f"\n 🔄 Workflow: {workflow.name}")
                for run in runs:
                    estado = run.conclusion or run.status
                    # Asignación de emojis según el estado real de GitHub Actions
                    if estado == "success":
                        emoji = "🟢 [OK]"
                    elif estado in ["failure", "cancelled"]:
                        emoji = "🔴 [FALLA]"
                    else:
                        emoji = "🟡 [EN PROCESO]"
                        
                    fecha = run.created_at.strftime("%Y-%m-%d %H:%M")
                    print(f"   {emoji} Run #{run.run_number} • {estado} • {fecha} • 🌿 {run.head_branch}")
    except GithubException:
        print(" ❌ No se pudieron cargar las ejecuciones de los workflows.")

    # 5. MÉTRICAS LOCALES
    separador("MÉTRICAS LOCALES DEL ÚLTIMO ENTRENAMIENTO")
    mostrar_metricas_locales()

    print(f"\n{'=' * 70}\n")
    github_client.close()


if __name__ == "__main__":
    main()