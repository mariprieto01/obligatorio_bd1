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
-- Table structure for table `actividades`
--

DROP TABLE IF EXISTS `actividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividades` (
  `idActividad` int NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `costo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idActividad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividades`
--

LOCK TABLES `actividades` WRITE;
/*!40000 ALTER TABLE `actividades` DISABLE KEYS */;
INSERT INTO `actividades` VALUES (123,'HOLA',10.20);
/*!40000 ALTER TABLE `actividades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumno_clase`
--

DROP TABLE IF EXISTS `alumno_clase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumno_clase` (
  `idClase` int NOT NULL,
  `ciAlumno` char(11) NOT NULL,
  `idEquipamiento` int NOT NULL,
  PRIMARY KEY (`idClase`,`ciAlumno`),
  KEY `ciAlumno` (`ciAlumno`),
  KEY `idEquipamiento` (`idEquipamiento`),
  CONSTRAINT `alumno_clase_ibfk_1` FOREIGN KEY (`idClase`) REFERENCES `clase` (`idClase`),
  CONSTRAINT `alumno_clase_ibfk_2` FOREIGN KEY (`ciAlumno`) REFERENCES `alumnos` (`ciAlumno`),
  CONSTRAINT `alumno_clase_ibfk_3` FOREIGN KEY (`idEquipamiento`) REFERENCES `equipamiento` (`idEquipamiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumno_clase`
--

LOCK TABLES `alumno_clase` WRITE;
/*!40000 ALTER TABLE `alumno_clase` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumno_clase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alumnos`
--

DROP TABLE IF EXISTS `alumnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumnos` (
  `ciAlumno` char(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `idActividad` int DEFAULT NULL,
  `alquila` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`ciAlumno`),
  KEY `idActividad` (`idActividad`),
  CONSTRAINT `alumnos_ibfk_1` FOREIGN KEY (`idActividad`) REFERENCES `actividades` (`idActividad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumnos`
--

LOCK TABLES `alumnos` WRITE;
/*!40000 ALTER TABLE `alumnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clase`
--

DROP TABLE IF EXISTS `clase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clase` (
  `idClase` int NOT NULL,
  `ciInstructor` char(11) NOT NULL,
  `idActividad` int NOT NULL,
  `idTurno` int NOT NULL,
  `dictada` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`idClase`),
  KEY `ciInstructor` (`ciInstructor`),
  KEY `idActividad` (`idActividad`),
  KEY `idTurno` (`idTurno`),
  CONSTRAINT `clase_ibfk_1` FOREIGN KEY (`ciInstructor`) REFERENCES `instructores` (`ciInstructor`),
  CONSTRAINT `clase_ibfk_2` FOREIGN KEY (`idActividad`) REFERENCES `actividades` (`idActividad`),
  CONSTRAINT `clase_ibfk_3` FOREIGN KEY (`idTurno`) REFERENCES `turnos` (`idTurno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clase`
--

LOCK TABLES `clase` WRITE;
/*!40000 ALTER TABLE `clase` DISABLE KEYS */;
/*!40000 ALTER TABLE `clase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipamiento`
--

DROP TABLE IF EXISTS `equipamiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipamiento` (
  `idEquipamiento` int NOT NULL,
  `idActividad` int NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `costo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idEquipamiento`),
  KEY `idActividad` (`idActividad`),
  CONSTRAINT `equipamiento_ibfk_1` FOREIGN KEY (`idActividad`) REFERENCES `actividades` (`idActividad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamiento`
--

LOCK TABLES `equipamiento` WRITE;
/*!40000 ALTER TABLE `equipamiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipamiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructores`
--

DROP TABLE IF EXISTS `instructores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructores` (
  `ciInstructor` char(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ciInstructor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructores`
--

LOCK TABLES `instructores` WRITE;
/*!40000 ALTER TABLE `instructores` DISABLE KEYS */;
/*!40000 ALTER TABLE `instructores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `correo` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`correo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnos`
--

DROP TABLE IF EXISTS `turnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turnos` (
  `idTurno` int NOT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  PRIMARY KEY (`idTurno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnos`
--

LOCK TABLES `turnos` WRITE;
/*!40000 ALTER TABLE `turnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `turnos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-08 18:41:13
-- DE PRUEBA
INSERT INTO `actividades` (`idActividad`, `descripcion`, `costo`)
VALUES
    (1, 'Curso de matematicas', 150.00),
    (2, 'Curso de programacion', 200.00),
    (3, 'Taller de fotografia', 120.50),
    (4, 'Clase de guitarra', 80.00),
    (5, 'Entrenamiento de futbol', 50.00);

INSERT INTO `alumnos` (`ciAlumno`, `nombre`, `apellido`, `fecha_nacimiento`, `idActividad`, `alquila`)
VALUES
    ('12345678901', 'Juan', 'Perez', '2000-05-15', 1, b'0'),
    ('23456789012', 'Maria', 'Gomez', '1998-11-22', 2, b'1'),
    ('34567890123', 'Carlos', 'Lopez', '2002-03-10', 3, b'0'),
    ('45678901234', 'Ana', 'Martinez', '1997-07-30', 4, b'1'),
    ('56789012345', 'Luis', 'Sanchez', '1999-12-05', 1, b'0');

INSERT INTO `instructores` (`ciInstructor`, `nombre`, `apellido`)
VALUES
    ('98765432109', 'Pedro', 'Lopez'),
    ('87654321098', 'Laura', 'Martinez'),
    ('76543210987', 'Miguel', 'Gonzalez'),
    ('65432109876', 'Lucia', 'Hernandez'),
    ('54321098765', 'David', 'Perez');

INSERT INTO `turnos` (`idTurno`, `hora_inicio`, `hora_fin`)
VALUES
    (1, '08:00:00', '10:00:00'),
    (2, '10:00:00', '12:00:00'),
    (3, '14:00:00', '16:00:00'),
    (4, '16:00:00', '18:00:00'),
    (5, '18:00:00', '20:00:00');


INSERT INTO `clase` (`idClase`, `ciInstructor`, `idActividad`, `idTurno`, `dictada`)
VALUES
    (1, '98765432109', 1, 1, b'1'),
    (2, '87654321098', 2, 2, b'0'),
    (3, '76543210987', 3, 3, b'1'),
    (4, '65432109876', 4, 1, b'0'),
    (5, '54321098765', 5, 2, b'1');


SELECT ciAlumno, nombre, apellido, fecha_nacimiento, descripcion,
CASE WHEN alquila = true THEN 'SI'
ELSE 'NO' END alquila
FROM alumnos
LEFT JOIN actividades ON actividades.idActividad = alumnos.idActividad
WHERE 1=1

SELECT FROM equipamiento
