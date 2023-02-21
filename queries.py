get_drinks_query = """
SELECT * FROM drink
"""

get_drink_by_id = """
SELECT * FROM drink WHERE drink_id = ?
"""

get_drink_by_name = """
SELECT * FROM drink WHERE drink_name = ?
"""

get_recipe_query = """
SELECT * FROM recipe WHERE drink_id = ?"""

get_an_ingredient_query = """
SELECT * FROM ingredient WHERE ingredient_id = ?
"""

get_ingredients_query = """
SELECT * FROM ingredient"""

create_drink_query = """
INSERT INTO drink (drink_name, price, method) VALUES(?, ?, ?)
"""

delete_drink_query = """
DELETE FROM drink WHERE drink_id = ?
"""

delete_recipe_query = """
DELETE FROM recipe WHERE drink_id = ?
"""

delete_ingredient_query = """
DELETE FROM ingredient WHERE ingredient_id = ?
"""

create_recipe_query = """
INSERT INTO recipe (drink_id, ingredient_id, measure_in_cl) VALUES (?, ?, ?)
"""

update_drink_query = """
UPDATE drink
SET drink_name =?, price = ?, method = ? 
WHERE drink_id = ?;
"""

create_ingredient_query = """
INSERT INTO ingredient (ingredient_name) VALUES (?)
"""
