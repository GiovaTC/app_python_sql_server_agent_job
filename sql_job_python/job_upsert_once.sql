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