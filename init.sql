-- for hairtiteapp database in psql

/*

-- Create a new user
CREATE USER <INSERT USER HERE> WITH PASSWORD '<INSERT PASSWORD HERE>';

-- Grant permissions on the database
GRANT CONNECT ON DATABASE hairtiteapp TO <INSERT USER HERE>;
GRANT USAGE ON SCHEMA public TO <INSERT USER HERE>;

-- Grant permissions on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <INSERT USER HERE>;

-- Grant default privileges on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO <INSERT USER HERE>;

*/

DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS franchises;

-- Create the Franchises table
CREATE TABLE franchises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create the Stores table
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    franchise INT NOT NULL,
    branch VARCHAR(100) NOT NULL,
    FOREIGN KEY (franchise) REFERENCES franchises(id)
);

-- Create the Staff table
CREATE TABLE staff (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    birthday DATE,
    store_id INT NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

-- Create the Scores table
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    staff_id INT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

-- Create a case-insensitive unique index on the email column
CREATE UNIQUE INDEX staff_email_lower_idx ON staff (LOWER(email));

-- Insert sample data into the franchises table
INSERT INTO franchises (name) VALUES ('McDonalds'), ('Starbucks'), ('Subway');

-- Insert sample data into the stores table
INSERT INTO stores (country, franchise, branch) VALUES
('United States', (SELECT id FROM franchises WHERE name = 'McDonalds'), 'Branch 1'),
('United Kingdom', (SELECT id FROM franchises WHERE name = 'Starbucks'), 'Branch 2'),
('Canada', (SELECT id FROM franchises WHERE name = 'Subway'), 'Branch 3'),
('Australia', (SELECT id FROM franchises WHERE name = 'McDonalds'), 'Branch 4'),
('Germany', (SELECT id FROM franchises WHERE name = 'Starbucks'), 'Branch 5');

-- Insert sample data into the staff table
INSERT INTO staff (full_name, email, birthday, store_id, password) VALUES
('John Doe', 'john.doe@example.com', '1985-05-15', (SELECT id FROM stores WHERE branch = 'Branch 1'), 'hashed_password_1'),
('Jane Smith', 'jane.smith@example.com', '1990-07-22', (SELECT id FROM stores WHERE branch = 'Branch 2'), 'hashed_password_2'),
('Alice Johnson', 'alice.johnson@example.com', '1988-11-30', (SELECT id FROM stores WHERE branch = 'Branch 3'), 'hashed_password_3'),
('Bob Brown', 'bob.brown@example.com', '1992-03-10', (SELECT id FROM stores WHERE branch = 'Branch 4'), 'hashed_password_4'),
('Carol White', 'carol.white@example.com', '1987-06-25', (SELECT id FROM stores WHERE branch = 'Branch 5'), 'hashed_password_5');

-- Insert sample data into the scores table
INSERT INTO scores (date, staff_id, score) VALUES
('2024-09-01 10:00:00', (SELECT id FROM staff WHERE email = 'john.doe@example.com'), 85),
('2024-09-01 11:00:00', (SELECT id FROM staff WHERE email = 'jane.smith@example.com'), 90),
('2024-09-01 12:00:00', (SELECT id FROM staff WHERE email = 'alice.johnson@example.com'), 78),
('2024-09-01 13:00:00', (SELECT id FROM staff WHERE email = 'bob.brown@example.com'), 82),
('2024-09-01 14:00:00', (SELECT id FROM staff WHERE email = 'carol.white@example.com'), 88);

/*

-- Grant USAGE and SELECT permissions on the sequence to the user
GRANT USAGE, SELECT ON SEQUENCE staff_id_seq TO <INSERT_USER_HERE>;

GRANT USAGE, SELECT ON SEQUENCE staff_id_seq TO <INSERT_USER_HERE>;

-- Grant USAGE and SELECT permissions on all sequences in the public schema
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO <INSERT_USER_HERE>;
*/