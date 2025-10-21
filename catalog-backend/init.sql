
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) NOT NULL,
    year int NOT NULL,
    description VARCHAR(250) DEFAULT 'No description given'
);

INSERT INTO courses (name, code, year, description) VALUES
('Programming', 'PRG101', 1, 'This is a course where you will have to make things by using a computer'),
('English', 'ENG201', 2, 'If you can read this description then you are eligible to take this course'),
('Microservice', 'INFS605', 2, 'This course seems familiar to you'),
('Math', 'MAT303', 3,'This is a third-year course where you do math and no its not maths'),
('Chemistry', 'CHE109', 1, 'Theres a lot of chemistry going on so you need to do nine courses of this in your first year');
