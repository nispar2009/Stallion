USE stallion

CREATE TABLE blog (id INTEGER PRIMARY KEY IDENTITY(1, 1), author VARCHAR(50), title VARCHAR(50), content VARCHAR(8000), topic VARCHAR(15), likes INT)
CREATE TABLE food (item VARCHAR(50) UNIQUE, cal INT, protein FLOAT, carbs FLOAT, fats FLOAT, na FLOAT)
CREATE TABLE ratings (author VARCHAR(50), comment VARCHAR(500), stars INT)
CREATE TABLE reported (id INTEGER PRIMARY KEY IDENTITY(1, 1), item VARCHAR(50), email VARCHAR(50))