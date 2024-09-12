-- for hairtiteapp database in psql

DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS franchises;

-- Create the Franchises table
CREATE TABLE franchises (
    franchise_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create the Stores table
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    franchise_id INT NOT NULL,
    branch VARCHAR(100) NOT NULL,
    FOREIGN KEY (franchise_id) REFERENCES franchises(franchise_id)
);

-- Create the Staff table
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    birthday DATE,
    store_id INT NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

-- Create the Scores table
CREATE TABLE scores (
    score_id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    staff_id INT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

-- Add learning resources table
CREATE TABLE learning_resources (
    resource_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    url VARCHAR(255) NOT NULL
);

CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer BOOLEAN NOT NULL,
    info TEXT NOT NULL,
    followup TEXT NOT NULL,
    fanswer BOOLEAN NOT NULL
);

-- Create a case-insensitive unique index on the email column
CREATE UNIQUE INDEX staff_email_lower_idx ON staff (LOWER(email));

-- Insert sample data into the franchises table
INSERT INTO franchises (name) VALUES ('McDonalds'), ('Starbucks'), ('Subway');

-- Insert sample data into the stores table
INSERT INTO stores (country, franchise_id, branch) VALUES
('United States', (SELECT franchise_id FROM franchises WHERE name = 'McDonalds'), 'Branch 1'),
('United Kingdom', (SELECT franchise_id FROM franchises WHERE name = 'Starbucks'), 'Branch 2'),
('Canada', (SELECT franchise_id FROM franchises WHERE name = 'Subway'), 'Branch 3'),
('Australia', (SELECT franchise_id FROM franchises WHERE name = 'McDonalds'), 'Branch 4'),
('Germany', (SELECT franchise_id FROM franchises WHERE name = 'Starbucks'), 'Branch 5');

-- Insert sample data into the staff table
INSERT INTO staff (full_name, email, birthday, store_id, password) VALUES
('John Doe', 'john.doe@example.com', '1985-05-15', (SELECT store_id FROM stores WHERE branch = 'Branch 1'), 'hashed_password_1'),
('Jane Smith', 'jane.smith@example.com', '1990-07-22', (SELECT store_id FROM stores WHERE branch = 'Branch 2'), 'hashed_password_2'),
('Alice Johnson', 'alice.johnson@example.com', '1988-11-30', (SELECT store_id FROM stores WHERE branch = 'Branch 3'), 'hashed_password_3'),
('Bob Brown', 'bob.brown@example.com', '1992-03-10', (SELECT store_id FROM stores WHERE branch = 'Branch 4'), 'hashed_password_4'),
('Carol White', 'carol.white@example.com', '1987-06-25', (SELECT store_id FROM stores WHERE branch = 'Branch 5'), 'hashed_password_5');

-- Insert sample data into the scores table
INSERT INTO scores (date, staff_id, score) VALUES
('2024-09-01 10:00:00', (SELECT staff_id FROM staff WHERE email = 'john.doe@example.com'), 85),
('2024-09-01 11:00:00', (SELECT staff_id FROM staff WHERE email = 'jane.smith@example.com'), 90),
('2024-09-01 12:00:00', (SELECT staff_id FROM staff WHERE email = 'alice.johnson@example.com'), 78),
('2024-09-01 13:00:00', (SELECT staff_id FROM staff WHERE email = 'bob.brown@example.com'), 82),
('2024-09-01 14:00:00', (SELECT staff_id FROM staff WHERE email = 'carol.white@example.com'), 88);

-- Insert learning resources
INSERT INTO learning_resources (title, description, url) VALUES
('Whys is it so important?', '- How do customers react to finding hair in their food?\n- How would you deal with it?\n- Watch this video to find out!', 'https://youtube.com/shorts/2fs8kYYEGlI?feature=share'),
('Why keep hair under wraps?', '- Why is it important to keep hair covered?\n- What are the risks of not doing so?\n- Watch this video to find out!', 'https://www.youtube.com/shorts/fLxARwbSFIU'),
('Public Reactions; Hair Found In My Food!', '- What’s your reaction?\n- See how different people handle this gross surprise!', 'https://www.youtube.com/shorts/VsQRan7hapo');

-- Insert into questions

INSERT INTO questions (question, answer, info, followup, fanswer)
VALUES
('During an average of 8 hour-shift we average human beings naturally shed 40 – 130 hairs every day.', true, 'An average of 40 -130 hair-shafts will be lost to natural cyclical processes per day.', 'The average human sheds up to 130 hairs naturally every day.', true),
('Modern styling & hair-care practices damages hair', true, 'A) Excessive heat - higher temperature from / of hair driers / styling tongues/straighteners\n\nB) Perm solutions, dyes / straightening chemicals – Trichologists believe', 'Using hot tools like dryers or straighteners and chemicals like perm solutions impacts hair contamination.', true),
('Washing and combing removes all residual hair?', false, '', 'Daily combed hair, well-groomed beard, neatly trimmed brows and daily showering prevent removal of all loose hairs.', false),
('Digested hair contained within foods will make you physically sick?', false, 'Hair is protein and can be digested!', 'If you eat hair, you are likely to be sick', false),
('digested hair contained within foods is likely to make you feel sick', true, 'In most people the thought makes people feel sick – can and in most people does trigger an emotional reaction \n\nMost people will stop eating and it will kill their appetite – AND they will stop eating', 'If you find hair in your meal, even if you don’t eat it you might feel sick.', true),
('Contact with the head can cause food poisoning?', true, 'All people – with good hygiene – sweaty areas of skin such as the scalp contain food poisoning pathogen Staphylocci Aureus. If you touch your hand and then food – whether your hand is gloved or not – you can transfer food poisoning pathogens to the food you serve to your customers. – it’s a fact!', 'If I scratch my head, it is possible I can cause food poisoning?', true),
('Your actions help prevent food poisoning?', true, '', 'How I work helps prevent food poisoning.', true),
('Short hair poses a greater risk of contamination?', true, 'Short hair is more likely to stand upright and protrude through gaps including needle holes in all knitted, woven particularly non-woven fabrics.\n\nShort hair is less easily seen than long hair and therefore, may fall into food unseen and when eating food seen as the food is closer to the eyes and mouth.', 'short hair has a greater risk of contamination than long hair?', true);

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

-- Grant USAGE and SELECT permissions on the sequence to the user
GRANT USAGE, SELECT ON SEQUENCE staff_staff_id_seq TO <INSERT_USER_HERE>;

GRANT USAGE, SELECT ON SEQUENCE staff_staff_id_seq TO <INSERT_USER_HERE>;

-- Grant USAGE and SELECT permissions on all sequences in the public schema
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO <INSERT_USER_HERE>;


INSERT INTO stores (country, franchise_id, branch) VALUES
('United Kingdom', (SELECT franchise_id FROM franchises WHERE name = 'McDonalds'), 'Ilkeston'),
('United Kingdom', (SELECT franchise_id FROM franchises WHERE name = 'McDonalds'), 'Long Eaton'),
*/