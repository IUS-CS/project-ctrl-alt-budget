CREATE DATABASE IF NOT EXISTS `ctrl-alt-budget`;
USE `ctrl-alt-budget`;

DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    CONSTRAINT fk_accounts_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    account_name VARCHAR(50) NOT NULL,
    account_type ENUM('type1', 'type2') NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);