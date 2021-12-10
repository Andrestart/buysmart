-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema buysmart
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema buysmart
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `buysmart`;
CREATE SCHEMA IF NOT EXISTS `buysmart` DEFAULT CHARACTER SET utf8 ;
USE `buysmart` ;

-- -----------------------------------------------------
-- Table `buysmart`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buysmart`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `nameproduct` VARCHAR(45) NULL,
  PRIMARY KEY (`idproduct`),
  UNIQUE INDEX `nameproduct_UNIQUE` (`nameproduct` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `buysmart`.`graphs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buysmart`.`graphs` (
  `idgraphs` INT NOT NULL AUTO_INCREMENT,
  `graphtype` VARCHAR(45) NULL,
  `graph` BLOB NULL,
  `product_idproduct` INT NOT NULL,
  PRIMARY KEY (`idgraphs`),
  UNIQUE INDEX `graphtype_UNIQUE` (`graphtype` ASC) VISIBLE,
  INDEX `fk_graphs_product_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_graphs_product`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `buysmart`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `buysmart`.`dia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buysmart`.`dia` (
  `idscrapdia` INT NOT NULL AUTO_INCREMENT,
  `namescrap` VARCHAR(800) NULL,
  `supermarket` VARCHAR(45) NULL,
  `link` VARCHAR(800) NULL,
  `price` DECIMAL(50) NULL,
  `product_idproduct` INT NOT NULL,
  PRIMARY KEY (`idscrapdia`),
  UNIQUE INDEX `supermarket_UNIQUE` (`supermarket` ASC) VISIBLE,
  INDEX `fk_dia_product1_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_dia_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `buysmart`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `buysmart`.`carrefour`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buysmart`.`carrefour` (
  `idscrapcarrefour` INT NOT NULL AUTO_INCREMENT,
  `namescrap` VARCHAR(800) NULL,
  `supermarket` VARCHAR(45) NULL,
  `link` VARCHAR(800) NOT NULL,
  `price` DECIMAL(50) NULL,
  `product_idproduct` INT NOT NULL,
  PRIMARY KEY (`idscrapcarrefour`, `link`),
  UNIQUE INDEX `supermarket_UNIQUE` (`supermarket` ASC) VISIBLE,
  INDEX `fk_carrefour_product1_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_carrefour_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `buysmart`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `buysmart`.`eroski`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `buysmart`.`eroski` (
  `idscraperoski` INT NOT NULL AUTO_INCREMENT,
  `namescrap` VARCHAR(800) NULL,
  `supermarket` VARCHAR(45) NULL,
  `link` VARCHAR(800) NOT NULL,
  `price` DECIMAL(50) NULL,
  `product_idproduct` INT NOT NULL,
  PRIMARY KEY (`idscraperoski`, `link`),
  UNIQUE INDEX `supermarket_UNIQUE` (`supermarket` ASC) VISIBLE,
  INDEX `fk_eroski_product1_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_eroski_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `buysmart`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
