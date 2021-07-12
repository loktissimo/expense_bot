CREATE TABLE `users` (
	`telegram_id` INT NOT NULL,
	`name` TEXT(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
	PRIMARY KEY (`telegram_id`)
);


CREATE TABLE `expense` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`text` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
	`telegram_id` INT NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`telegram_id`) REFERENCES users(`telegram_id`)
);
