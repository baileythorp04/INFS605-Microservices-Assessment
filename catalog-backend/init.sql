
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) NOT NULL,
    year int NOT NULL,
    description VARCHAR(250) DEFAULT 'No description given'
);

INSERT INTO courses (name, code, year, description) VALUES
('from catalog folder', 'FCF404', 4, 'No description given'),
('Programming', 'PRG101', 1, 'No description given'),
('English', 'ENG201', 2, 'No description given'),
('course 3', 'CRS3', 2, 'No description given'),
('course 4', 'CRS4', 3,'No description given'),
('course 5', 'CRS5', 1, 'No description given');
