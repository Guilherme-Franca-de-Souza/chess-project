-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: chess
-- ------------------------------------------------------
-- Server version	5.7.44

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
-- Dumping data for table `jogadores`
--

LOCK TABLES `jogadores` WRITE;
/*!40000 ALTER TABLE `jogadores` DISABLE KEYS */;
INSERT INTO `jogadores` VALUES (1,'Stockfish 1-0',1,0),(2,'Stockfish 1-1',1,1),(3,'Stockfish 2-0',2,0),(4,'Stockfish 2-1',2,1),(5,'Stockfish 3-0',3,0),(6,'Stockfish 3-1',3,1),(7,'Stockfish 4-0',4,0),(8,'Stockfish 4-1',4,1),(9,'Stockfish 5-0',5,0),(10,'Stockfish 5-1',5,1),(11,'Stockfish 6-0',6,0),(12,'Stockfish 6-1',6,1),(13,'Stockfish 7-0',7,0),(14,'Stockfish 7-1',7,1),(15,'Stockfish 8-0',8,0),(16,'Stockfish 8-1',8,1),(17,'Stockfish 9-0',9,0),(18,'Stockfish 9-1',9,1),(19,'Stockfish 10-0',10,0),(20,'Stockfish 10-1',10,1),(21,'Stockfish 11-0',11,0),(22,'Stockfish 11-1',11,1),(23,'Stockfish 12-0',12,0),(24,'Stockfish 12-1',12,1),(25,'Stockfish 13-0',13,0),(26,'Stockfish 13-1',13,1),(27,'Stockfish 14-0',14,0),(28,'Stockfish 14-1',14,1),(29,'Stockfish 15-0',15,0),(30,'Stockfish 15-1',15,1),(31,'Stockfish 16-0',16,0),(32,'Stockfish 16-1',16,1),(33,'Stockfish 17-0',17,0),(34,'Stockfish 17-1',17,1),(35,'Stockfish 18-0',18,0),(36,'Stockfish 18-1',18,1),(37,'Stockfish 19-0',19,0),(38,'Stockfish 19-1',19,1),(39,'Stockfish 20-0',20,0),(40,'Stockfish 20-1',20,1);
/*!40000 ALTER TABLE `jogadores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-25 14:29:30
