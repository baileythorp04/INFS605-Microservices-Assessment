
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    text VARCHAR(250) NOT NULL,
    reply VARCHAR(250) DEFAULT 'no reply given',
    feedback_status VARCHAR(20) DEFAULT 'open' CHECK (feedback_status IN ('open','resolved','replied','discarded'))
);

INSERT INTO feedback (student_name, email, text) VALUES
('John', 'John@email.com', 'I love this microservices architected website'),
('Joan', 'Joan@email.com', 'I like this microservices architected website'),
('Johnny', 'Johnny@email.com', 'I dislike this microservices architected website'),
('Jean', 'Jean@email.com', 'I hate this microservices architected website');