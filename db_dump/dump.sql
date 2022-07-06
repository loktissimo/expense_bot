-- SQL DUMP
CREATE DATABASE IF NOT EXISTS expense_bot;
USE expense_bot;

CREATE TABLE `expense` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `text` varchar(255) DEFAULT NULL,
  `telegram_id` bigint(10) NOT NULL,
  `accepted` tinyint(1) DEFAULT "1",
  `write_date` timestamp NULL DEFAULT NULL,
  `accept_date` timestamp NULL DEFAULT NULL
);

CREATE TABLE `users` (
  `telegram_id` bigint(10) PRIMARY KEY NOT NULL,
  `name` text NOT NULL,
  `tel` varchar(20) NOT NULL DEFAULT "no number"
);

ALTER TABLE `expense` ADD FOREIGN KEY (`telegram_id`) REFERENCES `users` (`telegram_id`);
