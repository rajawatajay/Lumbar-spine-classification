-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bcc
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

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
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,'Navdeep','tidora7085@kytstore.com','deleting accound','hey','2025-02-22 04:11:09');
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `p_details`
--

DROP TABLE IF EXISTS `p_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `p_details` (
  `p_ID` varchar(255) NOT NULL,
  `Firstname` varchar(200) DEFAULT NULL,
  `Lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`p_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `p_details`
--

LOCK TABLES `p_details` WRITE;
/*!40000 ALTER TABLE `p_details` DISABLE KEYS */;
INSERT INTO `p_details` VALUES ('03b50fe9-7b66-433e-ae46-b420f8f591c5','Navdeep','Doriya','tidora7085@kytstore.com',91,'Planttech pcj, Sitapura','Jaipur','N@v33p123'),('0bf2c9a0-f80e-409e-b886-3e9860dbf56a','Rahul','Sharma','rijnetoigjnetogin@gmail.com',2147483647,'Scout And Guide Office,JLN Marg,Bajaj Nagar','Jaipur','A@4345gfijhi12'),('0fdab3c0-4b7e-41c5-9615-b7ba8e7828d9','Admin ','Calm','lanen29994@prorsd.com',2147483645,'Scout And Guide Office,JLN Marg,Bajaj Nagar','Jaipur','Afjjisun@fnjni12^&'),('20c614f3-d9ff-4391-a00d-4e0f1a99f470','Kuldeep','Singh Tak','itzkuldeep2002@gmail.com',NULL,NULL,NULL,NULL),('46a2a0d2-ad7f-4e46-80c2-a5a4135dedaa',NULL,NULL,'tidora7085@kytstore.com',NULL,NULL,NULL,NULL),('c1727ba3-693b-493b-89f8-31378d5930a5','Ajay','Rajwat','nowaxac247@agiuse.com',2147483647,'Pushkar','Ajmer ','Aj@y123456Singh'),('c5b766d4-72a2-4a5f-b934-715ee882d6ad','Kuldeep','Singh Tak','Adminhead.01@calm.com',789745632,'Malviya nagar','Jaipur','J@1pur#KD'),('dd171e1f-3052-4169-8c65-2c8e47beeaa6','Ajay','Rajwat','natah90898@clubemp.com',2147483647,'Pushkar','Ajmer ','Aj@y#pushkar123'),('e8811623-76ba-4fb0-a620-85504c278d4f','Anurag','Anand Duvey','fshfoiergfoi@gmail.com',2147483645,'Scout And Guide Office,JLN Marg,Bajaj Nagar','Jaipur','Anur@g#123');
/*!40000 ALTER TABLE `p_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `session_data` text NOT NULL,
  `expiry` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-19 13:45:14
