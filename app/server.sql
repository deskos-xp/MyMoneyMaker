-- MariaDB dump 10.17  Distrib 10.4.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: mmm
-- ------------------------------------------------------
-- Server version	10.4.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Saved`
--

DROP TABLE IF EXISTS `Saved`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Saved` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pennies` int(11) DEFAULT NULL,
  `nickels` int(11) DEFAULT NULL,
  `dimes` int(11) DEFAULT NULL,
  `quarters` int(11) DEFAULT NULL,
  `dollar` int(11) DEFAULT NULL,
  `dollar5` int(11) DEFAULT NULL,
  `dollar10` int(11) DEFAULT NULL,
  `dollar20` int(11) DEFAULT NULL,
  `dollar50` int(11) DEFAULT NULL,
  `dollar100` int(11) DEFAULT NULL,
  `date` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Saved`
--

LOCK TABLES `Saved` WRITE;
/*!40000 ALTER TABLE `Saved` DISABLE KEYS */;
INSERT INTO `Saved` VALUES (1,0,0,0,0,0,0,0,0,0,0,'06/27/2020',1),(2,0,0,0,0,0,0,0,18,0,0,'06/27/2020',1),(3,0,0,0,0,0,0,0,18,0,1,'06/27/2020',1),(4,0,0,0,0,0,17,0,18,0,1,'06/27/2020',1),(5,0,0,0,0,0,17,3,18,0,1,'06/27/2020',1),(6,0,0,0,0,29,17,3,18,0,1,'06/27/2020',1),(7,62,6,13,12,29,17,3,18,0,1,'06/27/2020',1),(8,117,10,28,21,29,17,3,18,0,1,'06/27/2020',1),(9,184,16,49,21,29,17,3,18,0,1,'06/27/2020',1),(10,184,16,49,34,29,17,3,18,0,1,'06/27/2020',1),(11,253,16,69,34,29,17,3,18,0,1,'06/27/2020',1),(12,253,25,69,50,29,17,3,18,0,1,'06/27/2020',1),(13,305,31,82,65,29,17,3,18,0,1,'06/27/2020',1),(14,377,35,92,76,29,17,3,18,0,1,'06/27/2020',1),(15,377,35,92,76,29,17,3,18,0,1,'06/27/2020',1),(16,377,35,92,76,29,17,3,18,0,1,'06/27/2020',1),(17,377,35,92,76,29,17,3,18,0,1,'06/27/2020',1),(18,377,35,92,78,31,17,3,18,0,1,'6/28/2020',1),(19,377,35,92,78,31,17,3,18,0,1,'6/28/2020',1),(20,377,35,92,78,32,17,3,18,0,1,'6/28/2020',1),(21,377,35,92,78,31,17,3,18,0,1,'6/28/2020',1),(22,378,35,92,78,31,17,3,18,0,1,'6/30/2020',1),(23,385,35,94,79,31,17,3,18,0,1,'6/30/2020',1),(24,1,0,0,0,0,0,0,0,0,0,'07/09/2020',2),(25,385,35,94,79,31,17,3,8,0,1,'6/30/2020',1);
/*!40000 ALTER TABLE `Saved` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`active` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin','first_name','last_name','middle_name','admin@localhost','(804) 854-4057',1,'$6$rounds=656000$BLTntRw86PFN7rjR$2LeyyOuD0r7fdEMqSDWS6Ftny.giHfpeGZrGRjal.J5YAFprUNYtmOW.Wzuj8.NdozzleQUNi8K5Rh/Gu8kdr0'),(2,'admin','carl','Carl','Hirner','Joseph','k.j.hirner.wisdom@gmail.com','(804) 854-4057',1,'$6$rounds=656000$CimJ6gPJy5wrQxWb$8U1hor/LboqQBcKn/WV0BKxMrGRXAtq3eqmyN.P6/ygUvaJZjMeGo1Sz3CmNhRPfeACJ26UJSZ21dPaGNNqkV.');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-10 12:33:11
