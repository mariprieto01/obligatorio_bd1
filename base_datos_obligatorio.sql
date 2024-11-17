-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: obligatorio
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table actividades
--

DROP TABLE IF EXISTS actividades;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE actividades (
                             idActividad int NOT NULL,
                             descripcion varchar(100) DEFAULT NULL,
                             costo decimal(10,2) NOT NULL,
                             PRIMARY KEY (idActividad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table actividades
--

LOCK TABLES actividades WRITE;
/*!40000 ALTER TABLE actividades DISABLE KEYS */;
/*!40000 ALTER TABLE actividades ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table alumno_clase
--

DROP TABLE IF EXISTS alumno_clase;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE alumno_clase (
                              idClase int NOT NULL,
                              ciAlumno char(11) NOT NULL,
                              idEquipamiento int NOT NULL,
                              PRIMARY KEY (idClase,ciAlumno),
                              KEY ciAlumno (ciAlumno),
                              KEY idEquipamiento (idEquipamiento),
                              CONSTRAINT alumno_clase_ibfk_1 FOREIGN KEY (idClase) REFERENCES clase (idClase),
                              CONSTRAINT alumno_clase_ibfk_2 FOREIGN KEY (ciAlumno) REFERENCES alumnos (ciAlumno),
                              CONSTRAINT alumno_clase_ibfk_3 FOREIGN KEY (idEquipamiento) REFERENCES equipamiento (idEquipamiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table alumno_clase
--

LOCK TABLES alumno_clase WRITE;
/*!40000 ALTER TABLE alumno_clase DISABLE KEYS */;
/*!40000 ALTER TABLE alumno_clase ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table alumnos
--

DROP TABLE IF EXISTS alumnos;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE alumnos (
                         ciAlumno char(11) NOT NULL,
                         nombre varchar(50) DEFAULT NULL,
                         apellido varchar(50) DEFAULT NULL,
                         fecha_nacimiento date DEFAULT NULL,
                         idActividad int DEFAULT NULL,
                         alquila bit(1) NOT NULL DEFAULT b'0',
                         PRIMARY KEY (ciAlumno),
                         KEY idActividad (idActividad),
                         CONSTRAINT alumnos_ibfk_1 FOREIGN KEY (idActividad) REFERENCES actividades (idActividad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table alumnos
--

LOCK TABLES alumnos WRITE;
/*!40000 ALTER TABLE alumnos DISABLE KEYS */;
/*!40000 ALTER TABLE alumnos ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table clase
--

DROP TABLE IF EXISTS clase;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table clase
--

LOCK TABLES clase WRITE;
/*!40000 ALTER TABLE clase DISABLE KEYS */;
/*!40000 ALTER TABLE clase ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table equipamiento
--

DROP TABLE IF EXISTS equipamiento;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE equipamiento (
                              idEquipamiento int NOT NULL,
                              idActividad int NOT NULL,
                              descripcion varchar(100) DEFAULT NULL,
                              costo decimal(10,2) NOT NULL,
                              PRIMARY KEY (idEquipamiento),
                              KEY idActividad (idActividad),
                              CONSTRAINT equipamiento_ibfk_1 FOREIGN KEY (idActividad) REFERENCES actividades (idActividad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table equipamiento
--

LOCK TABLES equipamiento WRITE;
/*!40000 ALTER TABLE equipamiento DISABLE KEYS */;
/*!40000 ALTER TABLE equipamiento ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table instructores
--

DROP TABLE IF EXISTS instructores;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE instructores (
                              ciInstructor char(11) NOT NULL,
                              nombre varchar(50) DEFAULT NULL,
                              apellido varchar(50) DEFAULT NULL,
                              PRIMARY KEY (ciInstructor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table instructores
--

LOCK TABLES instructores WRITE;
/*!40000 ALTER TABLE instructores DISABLE KEYS */;
/*!40000 ALTER TABLE instructores ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table login
--

DROP TABLE IF EXISTS login;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE login (
                       nombre varchar(20) NOT NULL,
                       apellido varchar(20) NOT NULL,
                       email varchar(20) NOT NULL,
                       password varchar(20) NOT NULL,
                       PRIMARY KEY (email),
                       UNIQUE KEY email (email),
                       UNIQUE KEY password (password)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table login
--

LOCK TABLES login WRITE;
/*!40000 ALTER TABLE login DISABLE KEYS */;
/*!40000 ALTER TABLE login ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table turnos
--

DROP TABLE IF EXISTS turnos;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE turnos (
                        idTurno int NOT NULL,
                        hora_inicio time DEFAULT NULL,
                        hora_fin time DEFAULT NULL,
                        PRIMARY KEY (idTurno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table turnos
--

LOCK TABLES turnos WRITE;
/*!40000 ALTER TABLE turnos DISABLE KEYS */;
/*!40000 ALTER TABLE turnos ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-14 16:52:22

select * from login
insert into login values('admin','admin@email.com','admin','admin')
select * from alumnos

insert into actividades values(1,'Natacion',1000.0)
insert into actividades values(2,'Gimnasia',500.0)
insert into actividades values(3,'Crossfit',1500.0)

insert into alumnos values('12345678901','Juan','Perez','1990-01-01',1, 1)
insert into alumnos values('12345678902','Pedro','Gomez','1990-01-01',1, 0)
insert into alumnos values('12345678903','Maria','Rodriguez','1990-01-01',1, 1)

-- Insertando registros en la tabla instructores
INSERT INTO instructores (ciInstructor, nombre, apellido)
VALUES
    (101, 'Juan', 'Pérez'),
    (102, 'María', 'Gómez'),
    (103, 'Carlos', 'Rodríguez'),
    (104, 'Ana', 'Fernández'),
    (105, 'Luis', 'Martínez');
select * from instructores

INSERT INTO actividades (idActividad, descripcion, costo)
VALUES
    (4, 'Descripción de la actividad 4', 300.00);
    (2, 'Descripción de la actividad 2', 250.00);


INSERT INTO equipamiento (idActividad, idEquipamiento, descripcion, costo)
VALUES
    (4, 105, 'Descripción del artículo 4', 150.00);

select * from equipamiento
SELECT idEquipamiento, equipamiento.descripcion descripcion_equipamiento, actividades.descripcion descripcion_actividades, equipamiento.costo costo_equipamiento
FROM equipamiento
INNER JOIN actividades ON actividades.idActividad = equipamiento.idActividad
WHERE 1=1

select idClase, idTurno, dictada, descripcion, nombre
from clase
inner join actividades a on clase.idActividad = a.idActividad
inner join instructores i on clase.ciInstructor = i.ciInstructor;



INSERT INTO turnos (idTurno, hora_inicio, hora_fin)
VALUES
    (1, '08:00:00', '10:00:00'),
    (2, '10:00:00', '12:00:00'),
    (3, '14:00:00', '16:00:00'),
    (4, '16:00:00', '18:00:00');


INSERT INTO clase ( idClase, ciInstructor, idActividad, idTurno, dictada)
VALUES
    (109, 101, 3, 3, 0),
    (204, 102, 2, 4, 0);

select * from alumnos