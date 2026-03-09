CREATE DATABASE IF NOT EXISTS `ctrl-alt-budget`;
USE `ctrl-alt-budget`;

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);