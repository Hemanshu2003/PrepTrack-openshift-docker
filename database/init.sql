CREATE TABLE IF NOT EXISTS study_tasks (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'Pending'
);

INSERT INTO study_tasks (topic, description, status) VALUES 
('System Administration', 'Revise Linux and Windows server commands', 'In Progress'),
('Database Management', 'Practice advanced SQL queries and indexing', 'Pending'),
('Software Engineering', 'Review Python data structures and algorithms', 'Completed'),
('Containerization', 'Deploy multi-tier apps using Docker and Kubernetes', 'In Progress');


