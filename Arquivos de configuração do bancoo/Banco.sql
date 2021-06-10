CREATE DATABASE  IF NOT EXISTS `salas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `salas`;
-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: salas
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dia_semana`
--

DROP TABLE IF EXISTS `dia_semana`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia_semana` (
  `dia_semana` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dia_semana`
--

LOCK TABLES `dia_semana` WRITE;
/*!40000 ALTER TABLE `dia_semana` DISABLE KEYS */;
INSERT INTO `dia_semana` VALUES ('seg'),('ter'),('qua'),('qui'),('sex'),('sab');
/*!40000 ALTER TABLE `dia_semana` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horario`
--

DROP TABLE IF EXISTS `horario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horario` (
  `horario` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horario`
--

LOCK TABLES `horario` WRITE;
/*!40000 ALTER TABLE `horario` DISABLE KEYS */;
INSERT INTO `horario` VALUES (1),(2),(3),(4),(5),(6),(7),(8);
/*!40000 ALTER TABLE `horario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salas`
--

DROP TABLE IF EXISTS `salas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salas` (
  `id_sala` text,
  `numero_cadeiras` bigint DEFAULT NULL,
  `acessivel` bigint DEFAULT NULL,
  `qualidade` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salas`
--

LOCK TABLES `salas` WRITE;
/*!40000 ALTER TABLE `salas` DISABLE KEYS */;
INSERT INTO `salas` VALUES ('101',100,1,1),('201',100,1,2),('301',100,1,2),('401',100,0,3),('501',100,0,3),('102',70,1,1),('202',70,1,1),('302',70,1,2),('402',70,1,2),('502',70,0,3),('103',50,1,1),('203',50,1,1),('303',50,1,2),('403',50,0,3),('503',50,0,3),('104',30,1,1),('204',30,1,2),('304',30,0,3),('105',10,1,1),('205',10,1,2);
/*!40000 ALTER TABLE `salas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solucao`
--

DROP TABLE IF EXISTS `solucao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solucao` (
  `id_sala` text,
  `dia_semana` text,
  `horario` bigint DEFAULT NULL,
  `cod_turma` text,
  `id_turma` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solucao`
--

LOCK TABLES `solucao` WRITE;
/*!40000 ALTER TABLE `solucao` DISABLE KEYS */;
INSERT INTO `solucao` VALUES ('101','seg',3,'COMP0281',11),('101','qui',3,'COMP0281',11),('201','seg',5,'COMP0197',24),('201','seg',8,'COMP0347',37),('201','ter',4,'COMP0219',17),('201','qua',4,'COMP0222',28),('201','qua',5,'COMP0197',24),('201','qua',8,'COMP0347',37),('201','sex',5,'COMP0197',24),('201','sex',8,'COMP0347',37),('301','ter',2,'COMP0219',8),('301','ter',5,'COMP0279',19),('301','ter',8,'COMP0284',42),('301','qua',3,'COMP0219',8),('301','qui',5,'COMP0279',19),('301','qui',8,'COMP0284',42),('401','seg',6,'COMP0198',40),('401','seg',7,'COMP0257',44),('401','ter',4,'COMP0233',14),('401','ter',6,'COMP0213',22),('401','qua',6,'COMP0198',40),('401','qua',7,'COMP0257',44),('401','qui',4,'COMP0233',14),('401','qui',6,'COMP0213',22),('401','sex',4,'COMP0233',14),('401','sex',6,'COMP0198',40),('501','seg',1,'COMP0311',1),('501','qua',1,'COMP0311',1),('102','seg',6,'COMP0196',23),('302','ter',6,'COMP0337',25),('302','qui',4,'COMP0219',17),('302','qui',6,'COMP0337',25),('402','seg',4,'COMP0222',27),('402','ter',3,'COMP0203',9),('402','ter',5,'COMP0212',21),('402','qui',2,'COMP0203',9),('402','qui',5,'COMP0212',21),('502','seg',2,'COMP0197',7),('502','seg',3,'COMP0396',12),('502','seg',4,'COMP0396',26),('502','seg',6,'COMP0265',30),('502','seg',7,'COMP0217',38),('502','seg',8,'COMP0210',39),('502','qua',2,'COMP0197',7),('502','qua',3,'COMP0396',12),('502','qua',4,'COMP0396',26),('502','qua',6,'COMP0265',30),('502','qua',7,'COMP0217',38),('502','qua',8,'COMP0210',39),('502','sex',2,'COMP0197',7),('502','sex',3,'COMP0396',12),('502','sex',4,'COMP0396',26),('203','ter',7,'COMP306',43),('203','qui',7,'COMP306',43),('203','sex',5,'COMP306',43),('303','seg',5,'COMP0297',29),('303','ter',1,'COMP0212',4),('303','qua',5,'COMP0297',29),('303','qui',1,'COMP0212',4),('403','seg',2,'COMP0197',6),('403','seg',3,'COMP0279',10),('403','seg',5,'COMP0281',20),('403','ter',1,'COMP0250',2),('403','ter',3,'COMP0282',13),('403','ter',5,'COMP0250',31),('403','qua',1,'COMP0250',2),('403','qua',2,'COMP0197',6),('403','qua',3,'COMP0279',10),('403','qua',5,'COMP0281',20),('403','qua',6,'COMP0203',18),('403','qui',3,'COMP0282',13),('403','qui',5,'COMP0250',31),('403','sex',1,'COMP0197',6),('403','sex',3,'COMP0279',10),('403','sex',6,'COMP0203',18),('503','seg',5,'COMP0282',32),('503','qua',5,'COMP0282',32),('104','seg',1,'COMP0284',3),('104','qui',2,'COMP0284',3),('304','seg',6,'COMP0311',36),('304','ter',2,'COMP0198',5),('304','ter',5,'COMP220',33),('304','ter',6,'COMP0311',15),('304','ter',7,'COMP0211',45),('304','ter',8,'COMP0264',41),('304','qua',6,'COMP0311',36),('304','qui',1,'COMP0198',5),('304','qui',6,'COMP0311',15),('304','qui',7,'COMP0211',45),('304','qui',8,'COMP0264',41),('304','sex',7,'COMP0211',45),('105','sab',1,'COMP0221',16),('105','sab',2,'COMP0221',16),('205','qui',5,'COMP220',34),('205','sex',5,'COMP220',35);
/*!40000 ALTER TABLE `solucao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turmas`
--

DROP TABLE IF EXISTS `turmas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turmas` (
  `id_turma` bigint DEFAULT NULL,
  `disciplina` text,
  `professor` text,
  `dias_horario` text,
  `numero_alunos` bigint DEFAULT NULL,
  `curso` text,
  `periodo` bigint DEFAULT NULL,
  `acessibilidade` bigint DEFAULT NULL,
  `qualidade` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turmas`
--

LOCK TABLES `turmas` WRITE;
/*!40000 ALTER TABLE `turmas` DISABLE KEYS */;
INSERT INTO `turmas` VALUES (1,'COMP0311','Prof T','2M12-4M12',100,'EC',5,0,1),(2,'COMP0250','Prof G','3M12-4M12',42,'EC',4,0,1),(3,'COMP0284','Prof Y','2M12-5M34',7,'EC',3,0,1),(4,'COMP0212','Prof E','3M12-5M12',45,'EC',2,1,1),(5,'COMP0198','Prof E','3M34-5M12',30,'EC',5,0,3),(6,'COMP0197','Prof R','2M34-4M34-6M12',50,'EC',1,0,2),(7,'COMP0197','Prof S','2M34-4M34-6M34',55,'EC',1,0,1),(8,'COMP0219','Prof G','3M34-4M56',90,'EC',8,1,2),(9,'COMP0203','Prof M','3M56-5M34',8,'EC',5,1,2),(10,'COMP0279','Prof A','2M56-4M56-6M56',45,'EC',9,0,3),(11,'COMP0281','Prof E','2M56-5M56',25,'EC',2,1,1),(12,'COMP0396','Prof K','2M56-4M56-6M56',70,'EC',3,0,2),(13,'COMP0282','Prof T','3M56-5M56',50,'EC',2,0,3),(14,'COMP0233','Prof M','3T12-5T12-6T12',55,'CC',5,0,1),(15,'COMP0311','Prof A','3T56-5T56',30,'SI',5,0,2),(16,'COMP0221','Prof E','7M12-7M34',10,'SI',3,1,1),(17,'COMP0219','Prof B','3T12-5T12',66,'CC',3,0,1),(18,'COMP0203','Prof K','4T56-6T56',27,'CC',5,0,2),(19,'COMP0279','Prof I','3T34-5T34',91,'CC',7,1,1),(20,'COMP0281','Prof M','2T34-4T34',47,'CC',4,0,3),(21,'COMP0212','Prof B','3T34-5T34',55,'CC',2,0,2),(22,'COMP0213','Prof C','3T56-5T56',87,'SI',5,0,3),(23,'COMP0196','Prof K','2T56',55,'CC',1,1,1),(24,'COMP0197','Prof T','2T34-4T34-6T34',55,'CC',1,1,2),(25,'COMP0337','Prof G','3T56-5T56',55,'CC',1,1,1),(26,'COMP0396','Prof Y','2T12-4T12-6T12',33,'CC',6,0,3),(27,'COMP0222','Prof E','2T12',15,'CC',4,0,1),(28,'COMP0222','Prof E','4T12',15,'EC',5,0,1),(29,'COMP0297','Prof R','2T34-4T34',25,'CC',5,0,2),(30,'COMP0265','Prof S','2T56-4T56',65,'CC',6,0,1),(31,'COMP0250','Prof G','3T34-5T34',35,'CC',3,0,2),(32,'COMP0282','Prof S','2T34-4T34',25,'CC',7,0,1),(33,'COMP220','Prof L','3T34',10,'EC',4,0,2),(34,'COMP220','Prof L','5T34',10,'EC',4,0,2),(35,'COMP220','Prof L','6T34',10,'EC',4,0,2),(36,'COMP0311','Prof A','2T56-4T56',30,'SI',5,0,3),(37,'COMP0347','Prof D','2N34-4N34-6N34',90,'SI',5,1,1),(38,'COMP0217','Prof H','2N12-4N12',65,'SI',3,0,2),(39,'COMP0210','Prof J','2N34-4N34',55,'SI',1,0,1),(40,'COMP0198','Prof MT','2T56-4T56-6T56',55,'SI',1,0,1),(41,'COMP0264','Prof I','3N34-5N34',20,'SI',8,0,3),(42,'COMP0284','Prof I','3N34-5N34',90,'SI',7,1,2),(43,'COMP306','Prof Y','3N12-5N12-6T34',45,'SI',4,0,1),(44,'COMP0257','Prof A','2N12-4N12',55,'SI',9,0,2),(45,'COMP0211','Prof K','3N12-5N12-6N12',17,'SI',5,0,3);
/*!40000 ALTER TABLE `turmas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-08 14:52:05
