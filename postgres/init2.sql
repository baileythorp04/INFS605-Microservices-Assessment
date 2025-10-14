-- REM: *******************************************************************
-- REM: ***** Assignment 2: INFS605 Microservices Programming Project *****
-- REM: *******************************************************************
-- REM: * Purpose: Creating the PostGres SQL code needed to create the tables for the database*
-- REM: * Stephen Thorpe 9301663 *
-- REM: * Version: 1.7 (Sunday 24 August 2025) *

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) NOT NULL,
    description VARCHAR(250) DEFAULT 'No description given'
);

INSERT INTO courses (name, code, description) VALUES
('Programming', 'PRG101', 'No description given'),
('English', 'ENG201', 'No description given'),
('course 3', 'CRS3', 'No description given'),
('course 4', 'CRS4', 'No description given'),
('course 5', 'CRS5', 'No description given');