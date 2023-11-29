-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS fruta_dev_db;
CREATE USER IF NOT EXISTS 'fruta_dev'@'localhost' IDENTIFIED BY 'fruta_dev_pwd';
GRANT ALL PRIVILEGES ON `fruta_dev_db`.* TO 'fruta_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'fruta_dev'@'localhost';
FLUSH PRIVILEGES;
