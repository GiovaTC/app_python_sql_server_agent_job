# app_python_sql_server_agent_job
# 🚀 Upsert con SQL Server Job (ejecución única) + Python

el job se ejecuta una sola vez, en lugar de programarlo recurrente, lo configuramos como un **one-time job** (ejecución única).  
inclusive, desde Python podemos disparar el job manualmente despues de insertar en la tabla *staging*.

---

## 📂 Proyecto: Upsert con SQL Server Job (ejecución única) + Python

### 1️⃣ SQL Server: esquema

Igual que antes: tabla principal y *staging*.  
Guardalo como **`schema_job_once.sql`**:

```sql
IF DB_ID('PruebaPython') IS NULL
BEGIN
    CREATE DATABASE PruebaPython;
END
GO

USE PruebaPython;
GO

-- Tabla principal
IF OBJECT_ID('dbo.Usuarios', 'U') IS NOT NULL
    DROP TABLE dbo.Usuarios;
GO

CREATE TABLE dbo.Usuarios (
    Id     INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Edad   INT           NOT NULL,
    Email  NVARCHAR(150) NOT NULL UNIQUE
);
GO

-- Tabla staging
IF OBJECT_ID('dbo.Usuarios_Staging', 'U') IS NOT NULL
    DROP TABLE dbo.Usuarios_Staging;
GO

CREATE TABLE dbo.Usuarios_Staging (
    Nombre NVARCHAR(100) NOT NULL,
    Edad   INT           NOT NULL,
    Email  NVARCHAR(150) NOT NULL
);
GO

2️⃣ SQL Server Job (script de upsert)
este es el script que ejecutara el job una sola vez .
guardalo como job_upsert_once.sql:

sql

USE PruebaPython;
GO

BEGIN TRAN;

MERGE dbo.Usuarios AS target
USING dbo.Usuarios_Staging AS src
    ON target.Email = src.Email
WHEN MATCHED THEN
    UPDATE SET
        target.Nombre = src.Nombre,
        target.Edad   = src.Edad
WHEN NOT MATCHED THEN
    INSERT (Nombre, Edad, Email)
    VALUES (src.Nombre, src.Edad, src.Email);

TRUNCATE TABLE dbo.Usuarios_Staging;

COMMIT TRAN;

3️⃣ crear un job de una sola ejecucion
en sql server management studio (SSMS):
ve a sql server agent > jobs > new Job .

nombralo: Job_Usuarios_Upsert_Once .

En Steps, agrega un paso con el contenido de job_upsert_once.sql .
En Schedules, crea un schedule con opción One time (ejecución única) .
O simplemente no configures schedule y lo ejecutas manualmente o desde Python.

4️⃣ Python: insertar en staging + disparar el job
Aquí, Python inserta en Usuarios_Staging y luego ejecuta el job una sola vez .

guarda como app_job_once.py:

python
import pyodbc

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
    inserta en la tabla staging .
    """
    with pyodbc.connect(CONN_STR, autocommit=False) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO dbo.Usuarios_Staging (Nombre, Edad, Email) VALUES (?, ?, ?);",
                (nombre, edad, email)
            )
        conn.commit()
    print(f"[STAGING] Insertado: {nombre}, {edad}, {email}")

def ejecutar_job(job_name: str):
    """
    ejecuta un job de sql server agent manualmente (una sola vez) .
    """
    with pyodbc.connect(CONN_STR, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("EXEC msdb.dbo.sp_start_job ?", job_name)
    print(f"[JOB] disparado: {job_name}")

if __name__ == "__main__":
    # 1) inserta en staging
    insertar_staging("Carlos Pérez", 28, "carlos.perez@exam.com.co")
    insertar_staging("Carlos A. Pérez", 29, "carlos.perez@exam.com.co")

    # 2) ejecuta el job en una sola vez .
    ejecutar_job("Job_Usuarios_Upsert_Once")

5️⃣ ejecucion paso a paso
ejecuta schema_job_once.sql para preparar tablas .

crea el job en sql server agent con el contenido de job_upsert_once.sql .

corre la app python:

bash

python app_job_once.py
✅ Resultado
python inserta en Usuarios_Staging.
dispara el job una sola vez con sp_start_job .

consulta en sql:

sql

SELECT * FROM dbo.Usuarios;

veras que el job ya hizo el upsert y vacio la tabla staging . 🎯

📌 con este modelo:
el job solo corre cuando tu lo dispares (manual o desde python) .

los cambios estan confirmados en la base (COMMIT TRAN) .

no es recurrente , solo se ejecuta una vez por invocacion .
