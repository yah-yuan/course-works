创建reader表:
CREATE TABLE `BookManager`.`Reader` (
  `userID` INT NOT NULL,
  `password` VARCHAR(45) NOT NULL DEFAULT '123456',
  `name` VARCHAR(10) NOT NULL,
  `birthday` DATE NULL,
  `telephone` VARCHAR(11) NOT NULL,
  `sex` VARCHAR(5) NULL COMMENT '借阅者表',
  PRIMARY KEY (`userID`));

创建manager表:
CREATE TABLE `BookManager`.`manager` (
  `managerID` INT NOT NULL,
  `password` VARCHAR(45) NOT NULL DEFAULT '123456',
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`managerID`));

创建book表:
CREATE TABLE `BookManager`.`book` (
  `bookID` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `total` INT NULL,
  `onShelf` INT NULL,
  `type` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  PRIMARY KEY (`bookID`));

创建borrowInfo表:
CREATE TABLE `BookManager`.`borrowInfo` (
  `idborrowInfo` INT(11) NOT NULL,
  `userID` INT(11) NOT NULL,
  `bookID` INT(11) NOT NULL,
  `borrowDate` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `deadline` TIMESTAMP NULL,
  `returnDate` TIMESTAMP NULL,
  PRIMARY KEY (`idborrowInfo`),
  INDEX `fk_borrowInfo_1_idx` (`userID` ASC),
  INDEX `fk_borrowInfo_2_idx` (`bookID` ASC),
  CONSTRAINT `fk_borrowInfo_1`
    FOREIGN KEY (`userID`)
    REFERENCES `BookManager`.`reader` (`userID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_borrowInfo_2`
    FOREIGN KEY (`bookID`)
    REFERENCES `BookManager`.`book` (`bookID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

创建manageInfo表:
CREATE TABLE `BookManager`.`manageInfo` (
  `manageInfoID` INT NOT NULL,
  `managerID` INT(11) NOT NULL,
  `bookID` INT(11) NOT NULL,
  `amount` INT NULL,
  `operation` VARCHAR(45) NULL,
  `time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`manageInfoID`),
  INDEX `fk_manageInfo_1_idx` (`bookID` ASC),
  INDEX `fk_manageInfo_2_idx` (`managerID` ASC),
  CONSTRAINT `fk_manageInfo_1`
    FOREIGN KEY (`bookID`)
    REFERENCES `BookManager`.`book` (`bookID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_manageInfo_2`
    FOREIGN KEY (`managerID`)
    REFERENCES `BookManager`.`manager` (`managerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);