import requests
import os
from db import DB
from api import Drink, Recipe
from dotenv import load_dotenv

load_dotenv()

db = DB()

url =  os.getenv('url')

def printmenu():
    print(f"""
    {"Welcome!":-^30} 
    
    1. View the available drinks 
    2. Get a recipe 
    3. Add a new drink 
    4. Change a drink  
    5. Remove a drink 
    6. View ingredients 
    7. Add an ingredient
    8. Delete an ingredient 
    9. Exit

    {"":-^30}
    """)

def new_drink_input(drink_to_update: Drink = None):
    method = ""
    price = ""
    drink_name = ""
    while not drink_name:
        drink_name = input("Insert name of drink: ").strip()
        if drink_name == "" and drink_to_update:
            drink_name = drink_to_update.drink_name
            print("Drink name unchanged.")
        if not drink_name:
            print("Try again.")

    while not price.isdigit():
        price = input("Insert price of drink: ").strip()
        if price == "" and drink_to_update:
            print("Price unchanged.")
            price = drink_to_update.price
            break
        elif price == "":
            print("Try again.")
        elif not price.isdigit():
            print("Only numbers, please.")
    while method not in ("Stir", "Shake", "Build"):
        method = input("Set 'Stir', 'Shake' or 'Build': ").strip()
        if method == "" and drink_to_update:
            print("Method unchanged.")
            method = drink_to_update.method
            break
        elif method not in ("Stir", "Shake", "Build"):
            print("Please enter a valid option.")
    new_drink = Drink(drink_name = drink_name, price = price, method = method)
    return new_drink

def new_recipe_input(new_drink: Drink):
    operation_success = False
    new_ingredient_measures = []
    new_ingredient_ids = []
    while operation_success == False:
        view_ingredients()
        new_ingredients_input = input(f"Enter the numbers that corrispond to the ingredients in {new_drink.drink_name}, seperated with a space \nOR enter 'YES' to add new ingrediets: ").strip()
        # give the user the option to add new ingredients
        if new_ingredients_input.lower() == 'yes':
            create_ingredient()
        elif all([i.isdigit() for i in new_ingredients_input.split()]):
            operation_success = True
    ingredients = view_ingredients()
    # new_ingredients = [i for i in new_ingredients_input.split()]
    new_ingredients = [eval(i) for i in new_ingredients_input.split()]
    for item in new_ingredients:
        if item in range(1, len(ingredients) + 1):
            measure = ""
            while not measure:
                measure = input(f"Amount of {ingredients[item-1]['ingredient_name']} needed in cl: ").strip()
                if measure == "":
                    print("Failed to register. Try again.")
            new_ingredient_ids.append(ingredients[item-1]['ingredient_id'])
            new_ingredient_measures.append(int(measure))

    new_recipes = list(zip(new_ingredient_ids, new_ingredient_measures))
    return new_recipes

def view_drinks():
    res = requests.get(f"{url}/drinks")
    #convert respons to list of dicts
    data = res.json()
    # make each dict into a Drink-class object, using its kwargs
    for i, drink in enumerate(data):
        drink = Drink(**drink)
        print(f"Drink#: \t{i+1}")
        print(f"Drink: \t\t{drink.drink_name}")
        print(f"Price: \t\t{drink.price} SEK")
        print(f"Method: \t{drink.method}")
        print(f"{'-':-^35}")
    return data

def get_recipe(prompt: str = "Select a drink# to view: "):
    data = view_drinks()
    result: Drink = None
    operation_success = False
    drink_to_view = ""
    while operation_success == False:
        drink_to_view = input(prompt).strip()
        if not drink_to_view.isdigit():
            print("Only numbers, please")
        elif int(drink_to_view) not in range(1, len(data) + 1):
            print("Drink could not be retrieved. Are you sure it exists?")
        else:
            for i, drink in enumerate(data):
                if i+1 == int(drink_to_view):
                    drink_to_view = drink['drink_id']
                    result = Drink(**drink)
                    break
            res = requests.get(f"{url}/drinks/{drink_to_view}")
            if not res.status_code == 200:
                print("Drink could not be retrieved. Are you sure it exists?")
            else:
                operation_success = True
            data = res.json()
            drink_name = data[0]
            drink_ingredients = data[1]
            ingredient_measure = data[2]
            print(" ")
            print(f"{drink_name:-^30}")
            for i, ingredient in enumerate(drink_ingredients):
                print(f"{ingredient}: {ingredient_measure[i]} cl")
            print(" ")
    return result

def create_drink():
    new_drink = new_drink_input()
    requests.post(f"{url}/create_drink", json = new_drink.dict())
    new_recipes = []
    while not new_recipes:
        new_recipes = new_recipe_input(new_drink)
    new_drink = requests.get(f"{url}/drink_by_name/{new_drink.drink_name}", new_drink.drink_name).json()
    new_drink = Drink(**new_drink)
    for tuple in new_recipes:
        (ingredient_id, measure) = tuple
        recipe = Recipe(drink_id = new_drink.drink_id, ingredient_id = ingredient_id, measure_in_cl = measure)
        requests.post(f"{url}/set_recipe", json = recipe.dict())

def update_drink():
    drink_to_update = get_recipe("Choose a drink to update (ID#): ")
    updated_drink = new_drink_input(drink_to_update)
    updated_drink.drink_id = drink_to_update.drink_id
    requests.put(f"{url}/update_drink/{drink_to_update}", json = updated_drink.dict())
    new_recipes = new_recipe_input(updated_drink)
    # If new recipe provided: delete all existing connections from drinks to ingredients and set new ones.
    if new_recipes:
        requests.delete(f"{url}/delete_recipe/{drink_to_update.drink_id}")
        for tuple in new_recipes:
            (ingredient_id, measure) = tuple
            recipe = Recipe(drink_id = updated_drink.drink_id, ingredient_id = ingredient_id, measure_in_cl = measure)
            requests.post(f"{url}/set_recipe", json = recipe.dict())
    

def delete_drink():
    drink_to_delete = get_recipe("Enter the drink# to be deleted: ")
    res1 = requests.delete(f"{url}/delete_drink/{drink_to_delete.drink_id}")
    res2 = requests.delete(f"{url}/delete_recipe/{drink_to_delete.drink_id}")
    if res1.status_code == 200 and res2.status_code ==200:
        print("Successfully removed!")

def view_ingredients():
    ingredients: dict = requests.get(f"{url}/ingredients").json()
    print(f"{'Available ingredients:':-^30}\n")
    for i, ingredient in enumerate(ingredients):
        print(f"Ingredient #{i+1}: {ingredient['ingredient_name']} ")
    print(" ")
    print(f"{'':-^30}\n")
    return ingredients

def create_ingredient():
    new_ingredient_name = ""
    while new_ingredient_name.strip() == "":
        new_ingredient_name = input("Set new ingredient name: ").strip()
        if new_ingredient_name == "":
            print("No text entered. Try again.")
        else:
            data = {'ingredient_name': new_ingredient_name}
            res = requests.post(f"{url}/create_ingredient", json = data)
            if res.status_code == 200:
                print("Successfully added!")
                return data
            else: 
                print(f"Something went wrong. Status code: {res.status_code}")

def delete_ingredient(): 
    data = view_ingredients()
    operation_success = False
    while operation_success == False:
        ingredient_to_delete = input("Enter the ingredient# to delete: ").strip()
        if not ingredient_to_delete.isdigit():
            print("Only numbers please.")
        elif int(ingredient_to_delete) not in range(1, len(data) + 1):
            print("Ingredient could not be found. Are you sure it exists?")
        else:
            for i, ingredient in enumerate(data):
                if i+1 == int(ingredient_to_delete):
                    ingredient_to_delete = ingredient["ingredient_id"]
            res = requests.delete(f"{url}/delete_ingredient/{ingredient_to_delete}")
            if res.status_code == 200:
                print("Successfully removed!")
                operation_success = True
            else: 
                print(f"Something went wrong. Status code: {res.status_code}")
    

def main():
    
    printmenu()
    choice = input("Enter an option: ").strip()
    print("")
    if not (choice.isdigit() and 1<= int(choice) <= 9):
        print("Valid options are 1-9.")
        return

    match int(choice):
        case 1: 
            view_drinks()
            # return_to_menu()
        case 2:
            # view_drinks()
            get_recipe()
        case 3:
            create_drink()
        case 4:
            view_drinks()
            update_drink()
        case 5:
            delete_drink()
        case 6:
            view_ingredients()
        case 7:
            view_ingredients()
            create_ingredient()
        case 8:
            delete_ingredient()
        case 9:
            exit()
    input("Press enter to go back to menu.")
    os.system('cls')

while __name__ == "__main__":
    main()


# Dubbelkolla initiering
# Lägg upp på git
