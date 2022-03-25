/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ expense_bot /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE expense_bot;

DROP TABLE IF EXISTS expense;
CREATE TABLE `expense` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telegram_id` int(20) NOT NULL,
  `accepted` tinyint(1) DEFAULT '1',
  `write_date` timestamp NULL DEFAULT NULL,
  `accept_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `telegram_id` (`telegram_id`),
  CONSTRAINT `expense_ibfk_1` FOREIGN KEY (`telegram_id`) REFERENCES `users` (`telegram_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
  `telegram_id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tel` varchar(100) NOT NULL,
  PRIMARY KEY (`telegram_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
