-- Set up database


-- Create a table with the drinks
CREATE TABLE drink(
	drink_id INT IDENTITY(1,1) PRIMARY KEY,
	drink_name VARCHAR(30) NOT NULL,
	price INT NOT NULL,
	method VARCHAR(5),-- "shake", "stir", "build"
	CHECK (method IN ('shake','stir','build'))
);

CREATE TABLE ingredient(
	ingredient_id INT IDENTITY(1,1) PRIMARY KEY,
	ingredient_name VARCHAR(30) NOT NULL
);

-- Create a linked table that relates ingredients to drinks
CREATE TABLE recipe(
	drink_id INT NOT NULL,
	ingredient_id INT NOT NULL,
	measure_in_cl INT NOT NULL, -- number of cl used in a drink
	FOREIGN KEY(drink_id) REFERENCES drink(drink_id) ON DELETE CASCADE,
	FOREIGN KEY(ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE,
	CONSTRAINT PK_recipe PRIMARY KEY(drink_id, ingredient_id)
);

