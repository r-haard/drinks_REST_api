from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

import queries
from db import DB

app = FastAPI()
db = DB()

class Drink(BaseModel):
    drink_id: int = None
    drink_name: str
    price: int
    method: str

class Recipe(BaseModel):
    drink_id: int = None
    ingredient_id: int
    measure_in_cl: int

class Ingredient(BaseModel):
    ingredient_id: int = None
    ingredient_name: str

def convert_to_drink(response) -> List[Drink]:
    drinks = []
    for drink in response:
        drink_id, drink_name, price, method = drink
        drinks.append(Drink(
            drink_id = drink_id,
            drink_name = drink_name, 
            price = price, 
            method = method))
    return drinks

@app.get("/")
def root():
    return "Feeling thirsty?"

@app.get("/drink_by_id/{drink_id}")
def get_a_drink(drink_id: int):
    res = db.call_db(queries.get_drink_by_id, drink_id)
    drink = convert_to_drink(res)
    return drink[0]

@app.get("/drink_by_name/{drink_name}")
def get_a_drink(drink_name: str):
    res = db.call_db(queries.get_drink_by_name, drink_name)
    drink = convert_to_drink(res)
    return drink[0]

@app.get("/drinks") # kolla på response_model osv 
def get_drinks():
    res = db.call_db(queries.get_drinks_query)
    drinks = convert_to_drink(res)
    return drinks

@app.get("/drinks/{drink_id}")
def get_recipe(drink_id: int):
    # Iterate the drinks to get the drink_name.
    drinks = get_drinks()
    for drink in drinks:
        if drink.drink_id == drink_id:
            drink_name = drink.drink_name

    # make a list of the measurements of the ingredients. Third element of inner list.
    res = db.call_db(queries.get_recipe_query, drink_id)
    ingredient_measure_list = [element[2] for element in res]

    ingredient_list = []

    #get each string value for the relevant ingredients and append to a list
    for row in res:
        ingredient = db.call_db(queries.get_an_ingredient_query, row.ingredient_id)[0]
        ingredient_list.append(ingredient.ingredient_name)
    return drink_name, ingredient_list, ingredient_measure_list

    

@app.post("/create_drink")
# def create_drink(drink: Drink):
def create_drink(drink: Drink):
    # Check for doubles
    existing_drinks = get_drinks()
    for item in existing_drinks:
        if item.drink_name == drink.drink_name:
            print("There is alerdy a drink with that name.")
            return "There is alerdy a drink with that name."
    else:
        db.call_db(queries.create_drink_query, drink.drink_name, drink.price, drink.method)

@app.post("/set_recipe")
def set_recipe(recipe: Recipe):
    db.call_db(queries.create_recipe_query, recipe.drink_id, recipe.ingredient_id, recipe.measure_in_cl)

@app.put("/update_drink/{drink_id}")
def update_drink(drink: Drink):
    db.call_db(queries.update_drink_query, drink.drink_name, drink.price, drink.method, drink.drink_id)

@app.get("/ingredients")
def get_ingredients():
    res = db.call_db(queries.get_ingredients_query)

    ingredients = []
    for ingredient in res:        
        ingredient_id, ingredient_name = ingredient
        ingredients.append(Ingredient(
            ingredient_id = ingredient_id,
            ingredient_name = ingredient_name))
    return ingredients

@app.post("/create_ingredient")
def add_ingredient(ingredient: Ingredient):
    db.call_db(queries.create_ingredient_query, ingredient.ingredient_name)

@app.delete("/delete_recipe/{drink_id}")
def update_recipe(drink_id):
    db.call_db(queries.delete_recipe_query, drink_id)
    
@app.delete("/delete_drink/{drink_id}")
def delete_drink(drink_id):
    db.call_db(queries.delete_drink_query, drink_id)

@app.delete("/delete_ingredient/{ingredient_id}")
def delete_ingredient(ingredient_id: str):
    db.call_db(queries.delete_ingredient_query, ingredient_id)
