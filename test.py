import os
import sys
import random
import subprocess
from datetime import datetime, timedelta

# --- Lista de mensajes realistas para los commits ---
COMMIT_MESSAGES = [
    "Corregir error tipográfico en la documentación",
    "Actualizar archivo de configuración",
    "Mejorar rendimiento de la función",
    "Reestructurar nombres de variables",
    "Añadir validación que falta",
    "Actualizar README",
    "Corregir error menor",
    "Mejorar gestión de errores",
    "Añadir casos de prueba",
    "Optimizar bucle",
    "Actualizar dependencias",
    "Mejorar el registro",
    "Corregir formato",
    "Reestructurar código para mayor claridad",
    "Actualizar comentarios",
    "Mejorar documentación",
    "Corregir problema en casos extremos",
    "Reestructurar función auxiliar",
    "Mejorar consistencia",
    "Actualizar muestra de datos",
]

# --- Función para generar commits ---
def generate_commits(start_date: str, end_date: str, file_path: str = "data.txt"):
    # Convertir fechas
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start > end:
        print("❌ La fecha inicial no puede ser mayor que la final.")
        return

    current = start
    while current <= end:
        commits_today = random.randint(1, 15)  # número de commits por día
        times = []

        # Generar horas aleatorias sin repetir
        for _ in range(commits_today):
            hour = random.randint(9, 23)   # entre 9 AM y 11 PM
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            times.append(current.replace(hour=hour, minute=minute, second=second))

        # Orden ascendente
        times.sort()

        for commit_time in times:
            # Sobrescribir el archivo con una sola línea
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Update on {commit_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # Seleccionar un mensaje realista
            message = random.choice(COMMIT_MESSAGES)

            # Configurar la fecha del commit
            env = os.environ.copy()
            env["GIT_COMMITTER_DATE"] = commit_time.strftime("%Y-%m-%d %H:%M:%S")

            # Hacer add y commit
            subprocess.run(["git", "add", file_path])
            subprocess.run(
                ["git", "commit", "-m", message, "--date", commit_time.strftime("%Y-%m-%d %H:%M:%S")],
                env=env
            )

        current += timedelta(days=1)

    # Push final
    subprocess.run(["git", "push", "origin", "main"])
    print("✅ Commits generados y enviados con éxito.")


if __name__ == "__main__":
    arg_count = len(sys.argv) - 1  # número de argumentos dados (excluye el nombre del archivo)

    if arg_count == 0:
        # 0 => argv[1] y argv[2] es igual a la fecha actual
        hoy = datetime.now().strftime("%Y-%m-%d")
        generate_commits(hoy, hoy)

    elif arg_count == 1:
        # 1 => argv[1] y argv[2] es igual a la fecha dada
        fecha = sys.argv[1]
        generate_commits(fecha, fecha)

    elif arg_count == 2:
        # 2 => desde argv[1] hasta argv[2]
        fecha_inicio = sys.argv[1]
        fecha_fin = sys.argv[2]
        generate_commits(fecha_inicio, fecha_fin)

    else:
        print("Error: demasiados argumentos. Uso correcto:")
        print("  python test.py                # fecha actual")
        print("  python test.py YYYY-MM-DD     # fecha única")
        print("  python test.py YYYY-MM-DD YYYY-MM-DD  # rango de fechas")