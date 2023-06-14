-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema e-wallet
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema e-wallet
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `e-wallet` ;
USE `e-wallet` ;

-- -----------------------------------------------------
-- Table `e-wallet`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `is_admin` TINYINT(4) NOT NULL DEFAULT 0,
  `is_blocked` TINYINT(4) NOT NULL DEFAULT 0,
  `two_factor_method` ENUM('email', 'sms') NULL DEFAULT NULL,
  `anti_money_laundry_checked` TINYINT(4) NOT NULL DEFAULT 0,
  `email_verified` TINYINT(4) NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `stripe_id` VARCHAR(255) NULL DEFAULT NULL,
  `token` VARCHAR(255) NULL DEFAULT NULL,
  `title` ENUM('Mr', 'Mrs', 'Miss', 'Ms', 'Dr', 'Prof') NULL DEFAULT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `gender` ENUM('male', 'female', 'other') NOT NULL,
  `dob` DATE NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(10) NOT NULL,
  `photo_selfie` LONGBLOB NULL DEFAULT NULL,
  `identity_document` LONGBLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 11;


-- -----------------------------------------------------
-- Table `e-wallet`.`contacts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`contacts` (
  `user_id` INT(11) NOT NULL,
  `contact_id` INT(11) NOT NULL,
  PRIMARY KEY (`user_id`, `contact_id`),
  INDEX `fk_users_has_users_users2_idx` (`contact_id` ASC) ,
  INDEX `fk_users_has_users_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_users_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`contact_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`currencies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`currencies` (
  `id` TINYINT(4) NOT NULL,
  `currency` CHAR(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`wallets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`wallets` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NULL DEFAULT NULL,
  `balance` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `type` ENUM('personal', 'joint') NOT NULL,
  `is_active` TINYINT(4) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `default_wallet` TINYINT(4) NOT NULL DEFAULT 0,
  `creator_id` INT(11) NOT NULL,
  `currency_id` TINYINT(4) NOT NULL,
  `transaction_balance` DECIMAL(10,2) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_wallets_currencies1_idx` (`currency_id` ASC) ,
  INDEX `fk_wallets_users1_idx` (`creator_id` ASC) ,
  CONSTRAINT `fk_wallets_currencies1`
    FOREIGN KEY (`currency_id`)
    REFERENCES `e-wallet`.`currencies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_wallets_users1`
    FOREIGN KEY (`creator_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 5;


-- -----------------------------------------------------
-- Table `e-wallet`.`transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`transactions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `amount` DECIMAL(10,2) NOT NULL,
  `accepted_by_recipient` TINYINT(4) NOT NULL DEFAULT 0,
  `confirmed` TINYINT(4) NOT NULL DEFAULT 0,
  `sent_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `received_at` DATE NULL DEFAULT NULL,
  `is_recurring` TINYINT(4) NOT NULL DEFAULT 0,
  `recipient_id` INT(11) NULL DEFAULT NULL,
  `category` ENUM('Rent', 'Utilities', 'Food & Groceries', 'Transportation', 'Health & Fitness', 'Shopping & Entertainment', 'Travel', 'Education', 'Personal Care', 'Investments & Savings', 'Other') NULL DEFAULT NULL,
  `wallet_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_transactions_users1_idx` (`recipient_id` ASC) ,
  INDEX `fk_transactions_wallets2_idx` (`wallet_id` ASC) ,
  CONSTRAINT `fk_transactions_users1`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_transactions_wallets2`
    FOREIGN KEY (`wallet_id`)
    REFERENCES `e-wallet`.`wallets` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 13;


-- -----------------------------------------------------
-- Table `e-wallet`.`currency_conversions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`currency_conversions` (
  `base_currency_id` TINYINT(4) NOT NULL,
  `quote_currency_id` TINYINT(4) NOT NULL,
  `fx_rate` DECIMAL(10,2) NOT NULL,
  `transaction_id` INT(11) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  INDEX `fk_currencies_has_currencies_currencies2_idx` (`quote_currency_id` ASC) ,
  INDEX `fk_currencies_has_currencies_currencies1_idx` (`base_currency_id` ASC) ,
  INDEX `fk_currency_conversions_transactions1_idx` (`transaction_id` ASC) ,
  CONSTRAINT `fk_currencies_has_currencies_currencies1`
    FOREIGN KEY (`base_currency_id`)
    REFERENCES `e-wallet`.`currencies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_currencies_has_currencies_currencies2`
    FOREIGN KEY (`quote_currency_id`)
    REFERENCES `e-wallet`.`currencies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_currency_conversions_transactions1`
    FOREIGN KEY (`transaction_id`)
    REFERENCES `e-wallet`.`transactions` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`recurring_transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`recurring_transactions` (
  `transaction_id` INT(11) NOT NULL,
  `interval` INT(11) NOT NULL,
  `next_occurrence` DATE NOT NULL,
  `status` ENUM('active', 'paused', 'cancelled') NOT NULL DEFAULT 'active',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`transaction_id`),
  INDEX `fk_recurring_transactions_transactions1_idx` (`transaction_id` ASC) ,
  CONSTRAINT `fk_recurring_transactions_transactions1`
    FOREIGN KEY (`transaction_id`)
    REFERENCES `e-wallet`.`transactions` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`referrals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`referrals` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `expiry_date` DATE NOT NULL,
  `is_used` TINYINT(4) NOT NULL DEFAULT 0,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_referrals_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_referrals_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`transfers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`transfers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` ENUM('deposit', 'withdrawal') NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `wallet_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_transfers_wallets1_idx` (`wallet_id` ASC) ,
  CONSTRAINT `fk_transfers_wallets1`
    FOREIGN KEY (`wallet_id`)
    REFERENCES `e-wallet`.`wallets` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `e-wallet`.`users_wallets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-wallet`.`users_wallets` (
  `user_id` INT(11) NOT NULL,
  `wallet_id` INT(11) NOT NULL,
  `is_creator` TINYINT(4) NOT NULL DEFAULT 0,
  `added_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `access_level` ENUM('null', 'top_up_only', 'full') NULL DEFAULT 'full',
  PRIMARY KEY (`user_id`, `wallet_id`),
  INDEX `fk_users_has_wallets_wallets1_idx` (`wallet_id` ASC) ,
  INDEX `fk_users_has_wallets_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_users_has_wallets_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `e-wallet`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_wallets_wallets1`
    FOREIGN KEY (`wallet_id`)
    REFERENCES `e-wallet`.`wallets` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT IGNORE INTO `e-wallet`.`currencies` (`id`, `currency`)
VALUES
  (1, 'USD'),
  (2, 'EUR'),
  (3, 'GBP'),
  (4, 'JPY'),
  (5, 'CAD'),
  (6, 'AUD'),
  (7, 'TRY'),
  (8, 'BGN');

ALTER TABLE `e-wallet`.`currencies`
MODIFY COLUMN `currency` CHAR(8);