import json


def write_temp(text):
    json_out = open("temp.txt", "w")
    json_out.write(text)
    json_out.close()


def get_recipes():
    raw = open("raw.txt", "r").read()
    recipe = raw.split("recipe = {")[1]
    recipe = recipe.split("\n  },")[0]
    write_temp(recipe)
    recipes = recipe.split("\n    },")
    return(recipes)


def get_recipe_name(recipe):
    name = recipe.split('name = "')[1].split('",')[0].strip()
    return(name)


def get_recipe_details(recipe):
    if 'normal' in recipe:
        details = recipe.split('normal = {')[1].split('\n      },')[0].strip()
    else:
        details = recipe.strip()
    return(details)


def get_crafting_time(details):
    if "energy_required = " in details:
        time = details.split("energy_required = ")[1].split(",")[0]
    else:
        time = 0.5
    return(time)


def get_ingredients(details):
    if '\n      ingredients = {' in details:
        ingredients_raw = details.split(
            "ingredients = {")[1].split("\n      },")[0]
    else:
        ingredients_raw = details.split(
            "ingredients = {")[1].split("\n        },")[0]
    ingredients_raw = ingredients_raw.replace('{', '')
    ingredients_raw = ingredients_raw.replace('\n', ' ').replace('\t', ' ')
    ingredients_raw = ingredients_raw.replace(
        ' ', '<>').replace('><', '').replace('<>', ' ')
    ingredients_raw = ingredients_raw.split('},')
    ingredients = {}
    for raw_ingredient in ingredients_raw:
        raw_ingredient = raw_ingredient.replace('"', '').replace('}', '')
        raw_ingredient = raw_ingredient.replace(' ', '')
        ingredient = raw_ingredient.split(',')
        ingredients[ingredient[0]] = ingredient[1]
    return(ingredients)


def process_recipes(recipes):
    processed_recipes = {}
    for recipe in recipes:
        details = get_recipe_details(recipe)
        processed_recipes[get_recipe_name(recipe)] = {
            'name': get_recipe_name(recipe),
            # 'details': get_recipe_details(recipe),
            'time': get_crafting_time(details),
            'ingredients': get_ingredients(details)
        }
    return(processed_recipes)


def write_json(dicttext):
    with open('recipe.json', 'w') as json_file:
        json.dump(dicttext, json_file)


def raw_to_recipe_json():
    raw_recipes = get_recipes()
    recipes = process_recipes(raw_recipes)
    write_json(recipes)


raw_to_recipe_json()
