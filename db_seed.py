import pandas as pd

import queries
from db import DB
db = DB()

def load_csv(file: str):
    csv_data = pd.read_csv(file)
    csv_data = csv_data.values.tolist()
    return csv_data


# load drinks data 
csv_data = load_csv("db_setup/drinks_load.csv")
for row in csv_data:
    db.call_db(queries.create_drink_query, row[1], row[2], row[3])

# load ingredients data
csv_data = load_csv("db_setup/ingredients_load.csv")
for row in csv_data:
    db.call_db(queries.create_ingredient_query, row[1])


# load recipe data
csv_data = load_csv("db_setup/recipe_load.csv")
for row in csv_data:
    db.call_db(queries.create_recipe_query, row[0], row[1], row[2])
