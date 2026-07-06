-- Create users tables
-- depends:

CREATE TABLE `users` (
`id` int NOT NULL AUTO_INCREMENT,
`username` varchar(255) NOT NULL,
`passwords` varchar(255) NOT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;