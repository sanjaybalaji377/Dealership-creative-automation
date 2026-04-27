CREATE DATABASE IF NOT EXISTS dealership_creative_tool;
USE dealership_creative_tool;

DROP TABLE IF EXISTS generated_creatives;
DROP TABLE IF EXISTS creative_jobs;
DROP TABLE IF EXISTS dealerships;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_code VARCHAR(100) NOT NULL UNIQUE,
    account_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dealerships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    dealer_code VARCHAR(150) NOT NULL,
    dealer_name VARCHAR(150) NOT NULL,
    panel_path VARCHAR(500),
    logo_light_path VARCHAR(500),
    logo_dark_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE creative_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_uid VARCHAR(50) NOT NULL UNIQUE,
    background_file VARCHAR(500) NOT NULL,
    output_formats VARCHAR(255) NOT NULL,
    total_count INT DEFAULT 0,
    zip_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE generated_creatives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    dealership_id INT,
    output_format VARCHAR(100) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES creative_jobs(id),
    FOREIGN KEY (dealership_id) REFERENCES dealerships(id)
);

INSERT INTO users (name, email, password, role) VALUES
('Admin', 'admin@dealercreative.com', 'Admin@123', 'admin');

INSERT INTO accounts (account_code, account_name) VALUES
('Tata-dealers', 'Tata'),
('VW-dealers', 'Volkswagen');

INSERT INTO dealerships (account_id, dealer_code, dealer_name, panel_path, logo_light_path, logo_dark_path) VALUES
(1, 'Bellad-tata', 'Bellad Tata', 'assets/Dealership-panels/Tata-dealers/Bellad-tata/template.png', 'assets/Dealership-panels/Tata-dealers/Bellad-tata/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Bellad-tata/logo-dark.png'),
(1, 'Jasper-tata-delhi', 'Jasper Tata Delhi', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/template.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-delhi/logo-dark.png'),
(1, 'Jasper-tata-guntur', 'Jasper Tata Guntur', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/template.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-guntur/logo-dark.png'),
(1, 'Jasper-tata-hyderabad', 'Jasper Tata Hyderabad', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/template.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-hyderabad/logo-dark.png'),
(1, 'Jasper-tata-vijayawada', 'Jasper Tata Vijayawada', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/template.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vijayawada/logo-dark.png'),
(1, 'Jasper-tata-vizag', 'Jasper Tata Vizag', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/template.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jasper-tata-vizag/logo-dark.png'),
(1, 'Jayaraj-tata', 'Jayaraj Tata', 'assets/Dealership-panels/Tata-dealers/Jayaraj-tata/template.png', 'assets/Dealership-panels/Tata-dealers/Jayaraj-tata/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Jayaraj-tata/logo-dark.png'),
(1, 'Kaveri-tata', 'Kaveri Tata', 'assets/Dealership-panels/Tata-dealers/Kaveri-tata/template.png', 'assets/Dealership-panels/Tata-dealers/Kaveri-tata/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Kaveri-tata/logo-dark.png'),
(1, 'Lakshmi-tata', 'Lakshmi Tata', 'assets/Dealership-panels/Tata-dealers/Lakshmi-tata/template.png', 'assets/Dealership-panels/Tata-dealers/Lakshmi-tata/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Lakshmi-tata/logo-dark.png'),
(1, 'Shiva-tata', 'Shiva Tata', 'assets/Dealership-panels/Tata-dealers/Shiva-tata/template.png', 'assets/Dealership-panels/Tata-dealers/Shiva-tata/logo-light.png', 'assets/Dealership-panels/Tata-dealers/Shiva-tata/logo-dark.png'),
(1, 'true-sai', 'True Sai', 'assets/Dealership-panels/Tata-dealers/true-sai/template.png', 'assets/Dealership-panels/Tata-dealers/true-sai/logo-light.png', 'assets/Dealership-panels/Tata-dealers/true-sai/logo-dark.png'),
(2, 'VW-Apple', 'Vw Apple', 'assets/Dealership-panels/VW-dealers/VW-Apple/template.png', 'assets/Dealership-panels/VW-dealers/VW-Apple/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Apple/logo-dark.png'),
(2, 'VW-Autobhan', 'Vw Autobhan', 'assets/Dealership-panels/VW-dealers/VW-Autobhan/template.png', 'assets/Dealership-panels/VW-dealers/VW-Autobhan/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Autobhan/logo-dark.png'),
(2, 'VW-Bangalore', 'Vw Bangalore', 'assets/Dealership-panels/VW-dealers/VW-Bangalore/template.png', 'assets/Dealership-panels/VW-dealers/VW-Bangalore/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Bangalore/logo-dark.png'),
(2, 'VW-Dehradyun', 'Vw Dehradyun', 'assets/Dealership-panels/VW-dealers/VW-Dehradyun/template.png', 'assets/Dealership-panels/VW-dealers/VW-Dehradyun/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Dehradyun/logo-dark.png'),
(2, 'VW-Frontier', 'Vw Frontier', 'assets/Dealership-panels/VW-dealers/VW-Frontier/template.png', 'assets/Dealership-panels/VW-dealers/VW-Frontier/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Frontier/logo-dark.png'),
(2, 'VW-Gorakpur', 'Vw Gorakpur', 'assets/Dealership-panels/VW-dealers/VW-Gorakpur/template.png', 'assets/Dealership-panels/VW-dealers/VW-Gorakpur/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Gorakpur/logo-dark.png'),
(2, 'VW-Haldawani', 'Vw Haldawani', 'assets/Dealership-panels/VW-dealers/VW-Haldawani/template.png', 'assets/Dealership-panels/VW-dealers/VW-Haldawani/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Haldawani/logo-dark.png'),
(2, 'VW-Hubli', 'Vw Hubli', 'assets/Dealership-panels/VW-dealers/VW-Hubli/template.png', 'assets/Dealership-panels/VW-dealers/VW-Hubli/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Hubli/logo-dark.png'),
(2, 'VW-Jodhpur', 'Vw Jodhpur', 'assets/Dealership-panels/VW-dealers/VW-Jodhpur/template.png', 'assets/Dealership-panels/VW-dealers/VW-Jodhpur/logo-light.png', 'assets/Dealership-panels/VW-dealers/VW-Jodhpur/logo-dark.png');
