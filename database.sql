-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: change_bot
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `currency_id` int(11) NOT NULL,
  `balance` decimal(11,6) NOT NULL,
  `post_stamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `currency_id` (`currency_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `balance_transaction`
--

DROP TABLE IF EXISTS `balance_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `balance_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_user_id` int(11) NOT NULL,
  `from_currency_id` int(11) NOT NULL,
  `from_hash` varchar(255) NOT NULL,
  `from_amount` decimal(11,6) NOT NULL,
  `from_account_id` int(11) NOT NULL,
  `to_user_id` int(11) NOT NULL,
  `to_currency_id` int(11) NOT NULL,
  `to_hash` varchar(255) NOT NULL,
  `to_amount` decimal(11,6) NOT NULL,
  `to_account_id` int(11) NOT NULL,
  `rate` decimal(11,6) NOT NULL,
  `post_stamp` datetime NOT NULL,
  `tx_id` varchar(255) NOT NULL,
  `block_id` int(11) NOT NULL,
  `confirmations` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `from_user_id` (`from_user_id`),
  KEY `to_user_id` (`to_user_id`),
  KEY `from_currency_id` (`from_currency_id`),
  KEY `to_currency_id` (`to_currency_id`),
  KEY `from_account_id` (`from_account_id`),
  KEY `to_account_id` (`to_account_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `balance_transaction_ibfk_1` FOREIGN KEY (`from_user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_2` FOREIGN KEY (`to_user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_3` FOREIGN KEY (`from_currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_4` FOREIGN KEY (`to_currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_5` FOREIGN KEY (`from_account_id`) REFERENCES `account` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_6` FOREIGN KEY (`to_account_id`) REFERENCES `account` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `balance_transaction_ibfk_7` FOREIGN KEY (`status_id`) REFERENCES `bt_status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bt_status`
--

DROP TABLE IF EXISTS `bt_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bt_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `alias` varchar(10) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `currency_rate`
--

DROP TABLE IF EXISTS `currency_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `currency_rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency_rate` varchar(45) NOT NULL,
  `base_currency_id` int(11) NOT NULL,
  `ref_currency_id` int(11) NOT NULL,
  `rate` decimal(11,6) NOT NULL,
  `update_stamp` datetime NOT NULL,
  `expire_stamp` datetime NOT NULL,
  `expire` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ref_currency_id` (`ref_currency_id`),
  KEY `base_currency_id` (`base_currency_id`),
  CONSTRAINT `currency_rate_ibfk_1` FOREIGN KEY (`ref_currency_id`) REFERENCES `account` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `currency_rate_ibfk_2` FOREIGN KEY (`base_currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pay_system`
--

DROP TABLE IF EXISTS `pay_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `currency_id` int(11) NOT NULL,
  `post_stamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pay_system_1_idx` (`currency_id`),
  CONSTRAINT `fk_pay_system_1` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `base_currency_id` int(11) NOT NULL,
  `ref_currency_id` int(11) NOT NULL,
  `rate` decimal(11,6) NOT NULL,
  `min` decimal(11,6) NOT NULL,
  `max` decimal(11,6) NOT NULL,
  `message` text,
  `pay_system_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_rquest_1_idx` (`user_id`),
  KEY `fk_rquest_2_idx` (`base_currency_id`),
  KEY `fk_rquest_3_idx` (`ref_currency_id`),
  KEY `fk_rquest_4_idx` (`pay_system_id`),
  CONSTRAINT `fk_rquest_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_rquest_2` FOREIGN KEY (`base_currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_rquest_3` FOREIGN KEY (`ref_currency_id`) REFERENCES `currency` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_rquest_4` FOREIGN KEY (`pay_system_id`) REFERENCES `pay_system` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tg_id` int(11) NOT NULL,
  `phone` varchar(18) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `lang` char(2) NOT NULL,
  `post_stamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tg_id_UNIQUE` (`tg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-13 19:47:36
