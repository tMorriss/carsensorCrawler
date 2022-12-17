CREATE DATABASE carsensor_crawler;

CREATE TABLE carsensor_crawler.log (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    date DATE,
    name VARCHAR(30) NOT NULL,
    price INT NOT NULL ,
    year INT NOT NULL,
    mileage INT NOT NULL,
    PRIMARY KEY (id));
