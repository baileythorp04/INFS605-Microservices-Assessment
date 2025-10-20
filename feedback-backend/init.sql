
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    text VARCHAR(250) NOT NULL
);

INSERT INTO feedback (student_name, text) VALUES
('John', 'I love this'),
('John2', 'I like this'),
('John3', 'I dislike this'),
('John4', 'I hate this');