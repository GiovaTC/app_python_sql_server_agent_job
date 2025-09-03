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