-- fiorr hairtiteapp database in psql

/*

-- Create a new user
CREATE USER <INSERT USER HERE> WITH PASSWORD '<INSERT PASSWORD HERE>';

-- Grant permissions on the database
GRANT CONNECT ON DATABASE your_database TO flask_user;
GRANT USAGE ON SCHEMA public TO flask_user;

-- Grant permissions on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO flask_user;

-- Grant default privileges on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO flask_user;

*/

DROP TABLE IF EXISTS Scores;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Stores;
DROP TABLE IF EXISTS Franchises;

-- Create the Franchises table
CREATE TABLE Franchises (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE
);

-- Create the Stores table
CREATE TABLE Stores (
    ID SERIAL PRIMARY KEY,
    Country VARCHAR(100) NOT NULL,
    Franchise INT NOT NULL,
    Branch VARCHAR(100) NOT NULL,
    FOREIGN KEY (Franchise) REFERENCES Franchises(ID)
);

-- Create the Staff table
CREATE TABLE Staff (
    ID SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    Birthday DATE,
    storeID INT NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (storeID) REFERENCES Stores(ID)
);

-- Create the Scores table
CREATE TABLE Scores (
    ID SERIAL PRIMARY KEY,
    Date TIMESTAMP NOT NULL,
    staff_id INT NOT NULL,
    Score INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES Staff(ID)
);

-- Insert sample data into the Franchises table
INSERT INTO Franchises (Name) VALUES ('McDonalds'), ('Starbucks'), ('Subway');

-- Insert sample data into the Stores table
INSERT INTO Stores (Country, Franchise, Branch) VALUES
('United States', (SELECT ID FROM Franchises WHERE Name = 'McDonalds'), 'Branch 1'),
('United Kingdom', (SELECT ID FROM Franchises WHERE Name = 'Starbucks'), 'Branch 2'),
('Canada', (SELECT ID FROM Franchises WHERE Name = 'Subway'), 'Branch 3'),
('Australia', (SELECT ID FROM Franchises WHERE Name = 'McDonalds'), 'Branch 4'),
('Germany', (SELECT ID FROM Franchises WHERE Name = 'Starbucks'), 'Branch 5');

-- Insert sample data into the Staff table
INSERT INTO Staff (full_name, email, Birthday, storeID, password) VALUES
('John Doe', 'john.doe@example.com', '1985-05-15', (SELECT ID FROM Stores WHERE Branch = 'Branch 1'), 'hashed_password_1'),
('Jane Smith', 'jane.smith@example.com', '1990-07-22', (SELECT ID FROM Stores WHERE Branch = 'Branch 2'), 'hashed_password_2'),
('Alice Johnson', 'alice.johnson@example.com', '1988-11-30', (SELECT ID FROM Stores WHERE Branch = 'Branch 3'), 'hashed_password_3'),
('Bob Brown', 'bob.brown@example.com', '1992-03-10', (SELECT ID FROM Stores WHERE Branch = 'Branch 4'), 'hashed_password_4'),
('Carol White', 'carol.white@example.com', '1987-06-25', (SELECT ID FROM Stores WHERE Branch = 'Branch 5'), 'hashed_password_5');

-- Insert sample data into the Scores table
INSERT INTO Scores (Date, staff_id, Score) VALUES
('2024-09-01 10:00:00', (SELECT ID FROM Staff WHERE email = 'john.doe@example.com'), 85),
('2024-09-01 11:00:00', (SELECT ID FROM Staff WHERE email = 'jane.smith@example.com'), 90),
('2024-09-01 12:00:00', (SELECT ID FROM Staff WHERE email = 'alice.johnson@example.com'), 78),
('2024-09-01 13:00:00', (SELECT ID FROM Staff WHERE email = 'bob.brown@example.com'), 82),
('2024-09-01 14:00:00', (SELECT ID FROM Staff WHERE email = 'carol.white@example.com'), 88);