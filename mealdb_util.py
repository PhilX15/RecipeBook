import print_util
import requests
import string


def get_meal_by_id(id):
    req2 = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}')
    meal = req2.json()
    req2.close()

    return meal['meals'][0]

def get_all_recipes():
    all_meals = []

    for letter in string.ascii_lowercase:
        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?f={letter}')
        data = response.json()
        response.close()

        if data['meals']:
            all_meals.extend(data['meals'])

    return all_meals


def get_all_ingredients():
    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/list.php?i=list')
    data = response.json()
    response.close()

    all_ingredients = [ingredient['strIngredient'].lower() for ingredient in data['meals'] if ingredient['strIngredient']]

    return all_ingredients


def get_ingredients(meal):
    ingredients = {meal[f'strIngredient{i}'].lower(): meal[f'strMeasure{i}'] for i in range(1, 21) if meal[f'strIngredient{i}']}

    return ingredients
