
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) NOT NULL,
    description VARCHAR(250) DEFAULT 'No description given'
);

INSERT INTO courses (name, code, description) VALUES
('from catalog folder', 'FCF404', 'No description given'),
('Programming', 'PRG101', 'No description given'),
('English', 'ENG201', 'No description given'),
('course 3', 'CRS3', 'No description given'),
('course 4', 'CRS4', 'No description given'),
('course 5', 'CRS5', 'No description given');
