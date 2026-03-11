/*
NOTES:
-- temporarily droping tables for development
-- foreign keys like category_id and bill_id can be NULL (transactions and bills do not have to be associated with categories for example)
-- is_active BOOLEAN defaults to true
-- goals(target_date) left nullable (optional field)

CHANGES FROM ERD:
-- creation_date DATE -> created_at TIMESTAMP
-- color CHAR or ENUM -> I chose CHAR(7) for the time being which stores color hex codes
-- renamed status and type because they are reserved words

*/

CREATE DATABASE IF NOT EXISTS `ctrl_alt_budget`;
USE `ctrl_alt_budget`;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    CONSTRAINT fk_accounts_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    account_name VARCHAR(50) NOT NULL,
    account_type ENUM('savings', 'checking', 'credit') NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS goals (
    goal_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    account_id CHAR(36) DEFAULT NULL,
    CONSTRAINT fk_goals_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_goals_accounts FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    title VARCHAR(255) NOT NULL,
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    target_date DATE,
    goal_status ENUM('active', 'completed', 'paused') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    category_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    parent_id CHAR(36) DEFAULT NULL,
    CONSTRAINT fk_categories_users FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_categories_categories FOREIGN KEY (parent_id) REFERENCES categories(category_id),
    category_name VARCHAR(50) NOT NULL,
    category_type ENUM('income', 'expense') NOT NULL,
    color ENUM('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'teal', 'gray') NOT NULL
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
    frequency ENUM('daily', 'weekly', 'monthly', 'yearly') NOT NULL,
    next_due_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    account_id CHAR(36) NOT NULL,
    category_id CHAR(36) DEFAULT NULL,
    bill_id CHAR(36) DEFAULT NULL,
    CONSTRAINT fk_transactions_accounts FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    CONSTRAINT fk_transactions_categories FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT fk_transactions_bills FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    amount DECIMAL(15,2) NOT NULL,
    transaction_description TEXT,
    transaction_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);