import pyodbc

# Cadena de conexión a SQL Server
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=GTAPIERO-POLI;"
    "DATABASE=PruebaPython;"
    "UID=sa;"
    "PWD=tapiero;"
    "TrustServerCertificate=Yes;"
)

def insertar_staging(nombre: str, edad: int, email: str):
    """
    Inserta un registro en la tabla staging.
    """
    with pyodbc.connect(CONN_STR, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO dbo.Usuarios_Staging (Nombre, Edad, Email) VALUES (?, ?, ?);",
                (nombre, edad, email)
            )
    print(f"[STAGING] Insertado: {nombre}, {edad}, {email}")

def ejecutar_job(job_name: str):
    """
    Ejecuta un Job de SQL Server Agent manualmente (una sola vez).
    """
    with pyodbc.connect(CONN_STR, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("EXEC msdb.dbo.sp_start_job ?", job_name)
    print(f"[JOB] Disparado: {job_name}")

if __name__ == "__main__":
    # 1) Inserta en staging
    insertar_staging("Carlos Pérez", 28, "carlos.perez@exam.com.co")
    insertar_staging("Carlos A. Pérez", 29, "carlos.perez@exam.com.co")

    # 2) Ejecuta el Job una sola vez
    ejecutar_job("Job_Usuarios_Upsert_Once")
