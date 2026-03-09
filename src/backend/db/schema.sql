CREATE DATABASE IF NOT EXISTS `ctrl-alt-budget`;
USE `ctrl-alt-budget`;

DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Note: TEMPORARY ENUM types for account_type
CREATE TABLE IF NOT EXISTS accounts (
    account_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    CONSTRAINT fk_accounts_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    account_name VARCHAR(50) NOT NULL,
    account_type ENUM('type1', 'type2') NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS goals (
    goal_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    account_id CHAR(36) NOT NULL,
    CONSTRAINT fk_goals_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_goals_accounts FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    title VARCHAR(255) NOT NULL,
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    target_date DATE,
    goal_status ENUM('status1', 'status2') NOT NULL DEFAULT 'status1'
);

CREATE TABLE IF NOT EXISTS categories (
    category_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    parent_id CHAR(36) DEFAULT NULL,
    CONSTRAINT fk_categories_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_categories_categories FOREIGN KEY (parent_id) REFERENCES categories(category_id),
    category_name VARCHAR(50) NOT NULL,
    category_type ENUM('type1', 'type2') NOT NULL,
    color CHAR(7) DEFAULT '#ffffff'
);

CREATE TABLE IF NOT EXISTS bills (
    bill_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    account_id CHAR(36) NOT NULL,
    category_id CHAR(36) DEFAULT NULL,
    CONSTRAINT fk_bills_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_bills_accounts FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    CONSTRAINT fk_bills_categories FOREIGN KEY (category_id) REFERENCES categories(category_id),
    bill_name VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    frequency ENUM('frequency1', 'frequency2') NOT NULL,
    next_due_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);