CREATE DATABASE IF NOT EXISTS earthquake_db;
USE earthquake_db;

USE earthquake_db;

CREATE TABLE IF NOT EXISTS earthquakes (
    id VARCHAR(100) PRIMARY KEY,
    time DATETIME,
    updated DATETIME,
    mag DOUBLE,
    magType VARCHAR(20),
    place TEXT,
    type VARCHAR(50),
    status VARCHAR(20),
    tsunami TINYINT,
    sig INT,
    net VARCHAR(20),
    nst INT,
    dmin DOUBLE,
    rms DOUBLE,
    gap DOUBLE,
    magError DOUBLE,
    depthError DOUBLE,
    magNst INT,
    locationSource VARCHAR(50),
    magSource VARCHAR(50),
    alert VARCHAR(20),
    felt INT,
    cdi DOUBLE,
    mmi DOUBLE,
    types TEXT,
    title TEXT,
    ids TEXT,
    sources TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    depth_km DOUBLE,
    year INT,
    month INT,
    depth_category VARCHAR(30),
    country VARCHAR(100)
);
select * from earthquakes;



USE earthquake_db;

SET GLOBAL local_infile = 1;



SET GLOBAL local_infile = 1; -- need SUPER; if not allowed, skip and use Workbench wizard

SHOW VARIABLES LIKE 'local_infile';


LOAD DATA LOCAL INFILE '/Users/karthikeyan/Documents/Global Sesimic/data/earthquakes_clean_utf8.csv'
INTO TABLE earthquakes
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, time, updated, mag, magType, place, type, status, tsunami, sig, net, nst, dmin, rms, gap, magError, depthError, magNst, locationSource, magSource, alert, felt, cdi, mmi, types, title, ids, sources, latitude, longitude, depth_km, year, month, depth_category);
