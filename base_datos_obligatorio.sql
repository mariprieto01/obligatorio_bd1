-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
-- Host: localhost    Database: obligatorio
-- Server version	8.0.37

USE obligatorio;

DROP TABLE IF EXISTS actividades;
CREATE TABLE actividades (
    idActividad int NOT NULL,
    descripcion varchar(100) DEFAULT NULL,
    costo decimal(10,2) NOT NULL,
    restriccionEdad int NOT NULL,
    PRIMARY KEY (idActividad)
);

DROP TABLE IF EXISTS alumnos;
CREATE TABLE alumnos (
    ciAlumno char(11) NOT NULL,
    nombre varchar(50) DEFAULT NULL,
    apellido varchar(50) DEFAULT NULL,
    fecha_nacimiento date DEFAULT NULL,
    PRIMARY KEY (ciAlumno)
);

DROP TABLE IF EXISTS instructores;
CREATE TABLE instructores (
    ciInstructor char(11) NOT NULL,
    nombre varchar(50) DEFAULT NULL,
    apellido varchar(50) DEFAULT NULL,
    PRIMARY KEY (ciInstructor)
);

DROP TABLE IF EXISTS turnos;
CREATE TABLE turnos (
    idTurno int NOT NULL,
    hora_inicio time DEFAULT NULL,
    hora_fin time DEFAULT NULL,
    PRIMARY KEY (idTurno)
);

DROP TABLE IF EXISTS clase;
CREATE TABLE clase (
    idClase int NOT NULL,
    ciInstructor char(11) NOT NULL,
    idActividad int NOT NULL,
    idTurno int NOT NULL,
    dictada bit(1) NOT NULL DEFAULT b'0',
    PRIMARY KEY (idClase),
    KEY ciInstructor (ciInstructor),
    KEY idActividad (idActividad),
    KEY idTurno (idTurno),
    CONSTRAINT clase_ibfk_1 FOREIGN KEY (ciInstructor) REFERENCES instructores (ciInstructor),
    CONSTRAINT clase_ibfk_2 FOREIGN KEY (idActividad) REFERENCES actividades (idActividad),
    CONSTRAINT clase_ibfk_3 FOREIGN KEY (idTurno) REFERENCES turnos (idTurno)
);

DROP TABLE IF EXISTS equipamiento;
CREATE TABLE equipamiento (
    idEquipamiento int NOT NULL,
    idActividad int NOT NULL,
    descripcion varchar(100) DEFAULT NULL,
    costo decimal(10,2) NOT NULL,
    PRIMARY KEY (idEquipamiento),
    KEY idActividad (idActividad),
    CONSTRAINT equipamiento_ibfk_1 FOREIGN KEY (idActividad) REFERENCES actividades (idActividad)
);

DROP TABLE IF EXISTS alumno_clase;
CREATE TABLE alumno_clase (
    idClase int NOT NULL,
    ciAlumno char(11) NOT NULL,
    idEquipamiento int,
    PRIMARY KEY (idClase,ciAlumno),
    KEY ciAlumno (ciAlumno),
    KEY idEquipamiento (idEquipamiento),
    CONSTRAINT alumno_clase_ibfk_1 FOREIGN KEY (idClase) REFERENCES clase (idClase),
    CONSTRAINT alumno_clase_ibfk_2 FOREIGN KEY (ciAlumno) REFERENCES alumnos (ciAlumno),
    CONSTRAINT alumno_clase_ibfk_3 FOREIGN KEY (idEquipamiento) REFERENCES equipamiento (idEquipamiento)
);

DROP TABLE IF EXISTS login;
CREATE TABLE login (
    nombre varchar(20) NOT NULL,
    apellido varchar(20) NOT NULL,
    email varchar(20) NOT NULL,
    password varchar(20) NOT NULL,
    rol VARCHAR(15) DEFAULT NULL,
    PRIMARY KEY (email),
    UNIQUE KEY email (email),
    UNIQUE KEY password (password)
);

INSERT INTO alumnos(ciAlumno, nombre, apellido, fecha_nacimiento)
VALUES
    ('12345678901','Juan','Perez','1990-01-01'),
    ('12345678902','Pedro','Gomez','1990-01-01'),
    ('12345678903','Maria','Rodriguez','1990-01-01');

INSERT INTO instructores (ciInstructor, nombre, apellido)
VALUES
    (101, 'Juan', 'Pérez'),
    (102, 'María', 'Gómez'),
    (103, 'Carlos', 'Rodríguez'),
    (104, 'Ana', 'Fernández'),
    (105, 'Luis', 'Martínez');

INSERT INTO actividades (idActividad, descripcion, costo, restriccionEdad)
VALUES
    (1, 'Snowboard', 300.00, 10),
    (2, 'Ski', 250.00, 12),
    (3, 'Moto de nieve', 250.00, 15);

INSERT INTO equipamiento (idActividad, idEquipamiento, descripcion, costo)
VALUES
    (1, 1, 'Tabla de snowboard', 180.00),
    (2, 2, 'Esquíes', 150.00),
    (3, 3, 'Antiparras', 100.00);

SELECT idEquipamiento, equipamiento.descripcion descripcion_equipamiento, actividades.descripcion descripcion_actividades, equipamiento.costo costo_equipamiento
FROM equipamiento
INNER JOIN actividades ON actividades.idActividad = equipamiento.idActividad
WHERE 1=1;

SELECT idClase, idTurno, dictada, descripcion, nombre
FROM clase
INNER JOIN actividades a on clase.idActividad = a.idActividad
INNER JOIN instructores i on clase.ciInstructor = i.ciInstructor;

INSERT INTO turnos (idTurno, hora_inicio, hora_fin)
VALUES
    (1, '08:00:00', '10:00:00'),
    (2, '10:00:00', '12:00:00'),
    (3, '14:00:00', '16:00:00'),
    (4, '16:00:00', '18:00:00');

INSERT INTO clase ( idClase, ciInstructor, idActividad, idTurno, dictada)
VALUES
    (1, 103, 3, 3, 1),
    (109, 101, 3, 3, 0),
    (204, 102, 2, 1, 0);

INSERT INTO alumno_clase (idClase, ciAlumno, idEquipamiento)
VALUES
    (1, '12345678901', 3),
    (109, '12345678903', 3),
    (204, '12345678901', 2);

-- Insert de usuario con rol de administrador para que tenga acceso al sistema --
INSERT INTO login
VALUE
    ('Administrador','Administrador','admin@gmail.com','admin', 'administrador');
