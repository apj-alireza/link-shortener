-- Create links tables
-- depends:

CREATE TABLE `links` (
`id` binary(16) NOT NULL DEFAULT (uuid_to_bin(uuid())),
`user_id` int NOT NULL,
`destination_url` varchar(255) NOT NULL,
`slug` varchar(255) NOT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
`updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
KEY `user_id` (`user_id`),
CONSTRAINT `links_ibfk_1`
FOREIGN KEY (`user_id`)
REFERENCES `users` (`id`)
ON DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;